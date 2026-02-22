from flask import Blueprint, request, jsonify
from app import db
from app.modelos.models import ProcesoContractual, ItemProceso, Colegio, Proveedor # Ajusta la ruta a tus modelos
from datetime import datetime
import io
import os
from flask import current_app, send_file
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from datetime import datetime
from jinja2 import Environment
import zipfile
import re
from io import BytesIO
try:
    from docx2pdf import convert
    import pythoncom
except ImportError:
    pass

# Definimos el Blueprint
procesos_bp = Blueprint('procesos', __name__)

@procesos_bp.route('/guardar_proceso/<int:colegio_id>', methods=['POST'])
def guardar_proceso(colegio_id):
    try:
        data = request.get_json()
        
        # Función auxiliar para manejar fechas vacías
        def parse_date(date_str):
            if not date_str:
                return None
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return None

        # 1. Creamos la cabecera del proceso (SIN los campos eliminados)
        nuevo_proceso = ProcesoContractual(
            colegio_id=colegio_id,
            proveedor_id=data.get('proveedor_id'),
            vigencia=data.get('vigencia'),
            tipo_contrato=data.get('tipo_contrato'),
            objeto_desc=data.get('objeto_desc'),
            
            # Cronograma
            f_elaboracion=parse_date(data.get('f_elaboracion')),
            f_publicacion=parse_date(data.get('f_publicacion')),
            f_recepcion=parse_date(data.get('f_recepcion')),
            f_cierre=parse_date(data.get('f_cierre')),
            f_verificacion=parse_date(data.get('f_verificacion')),
            f_firma=parse_date(data.get('f_firma')),
            plazo_txt=data.get('plazo_txt'),
            
            # Información CDP (Campos simplificados)
            cdp_numero=data.get('cdp_numero'),
            cod_presupuestal=data.get('cod_presupuestal')
        )

        db.session.add(nuevo_proceso)
        db.session.flush() # Obtenemos el ID para asociar los ítems

        # 2. Guardamos los ítems de la tabla incluyendo el Código Clasificador
        items = data.get('items', [])
        for item in items:
            # Validamos que la descripción no esté vacía para evitar filas basura
            descripcion = item.get('descripcion', '').strip()
            if descripcion:
                nuevo_item = ItemProceso(
                    proceso_id=nuevo_proceso.id,
                    cantidad=float(item.get('cantidad') or 0),
                    codigo_clasificador=item.get('codigo_clasificador'), # <--- NUEVO CAMPO
                    descripcion=descripcion,
                    v_unitario=float(item.get('v_unitario') or 0),
                    v_total=float(item.get('v_total') or 0)
                )
                db.session.add(nuevo_item)

        db.session.commit()
        return jsonify({
            "status": "success", 
            "message": "Expediente guardado correctamente",
            "proceso_id": nuevo_proceso.id
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar proceso: {str(e)}") # Útil para debug en consola
        return jsonify({"status": "error", "message": "No se pudo guardar el proceso. Revise los datos."}), 500

@procesos_bp.route('/descargar_documentos/<int:proceso_id>')
def descargar_documentos(proceso_id):
    formato = request.args.get('formato', 'word').lower() 
    modo = request.args.get('modo', 'zip').lower() 

    try:
        # 1. Obtener datos
        proceso = ProcesoContractual.query.get_or_404(proceso_id)
        colegio = Colegio.query.get(proceso.colegio_id)
        proveedor = Proveedor.query.get(proceso.proveedor_id)

        nombre_col_limpio = re.sub(r'[^\w\s-]', '', colegio.nombre).replace(" ", "_").upper()

        # 2. Preparar ítems
        items_tabla = []
        total_acumulado = 0
        items_query = proceso.detalles_items if hasattr(proceso, 'detalles_items') else proceso.details_items
        
        for item in items_query:
            cant_limpia = int(item.cantidad) if item.cantidad % 1 == 0 else item.cantidad
            items_tabla.append({
                'cant': cant_limpia,
                'cod': str(item.codigo_clasificador or '').strip(),
                'desc': str(item.descripcion or '').strip(),
                'unit': f"{item.v_unitario:,.0f}",
                'total': f"{item.v_total:,.0f}"
            })
            total_acumulado += item.v_total

        # 3. Lógica de nombre contratista
        if proveedor.razon_social and not str(proveedor.razon_social).isdigit():
            nombre_final = proveedor.razon_social
        else:
            nombre_final = f"{proveedor.primer_nombre or ''} {proveedor.primer_apellido or ''}".strip()

        # 4. Crear el Contexto
        contexto = {
            'col_nombre': colegio.nombre.upper(),
            'col_nit': colegio.nit,
            'col_municipio': colegio.municipio,
            'col_rector': colegio.rector_nombre,
            'vigencia': proceso.vigencia,
            'tipo_contrato': proceso.tipo_contrato,
            'objeto': proceso.objeto_desc,
            'contratista': nombre_final.upper(),
            'doc_contratista': proveedor.documento,
            'cdp_numero': proceso.cdp_numero,
            'cod_presupuestal': proceso.cod_presupuestal,
            'f_elaboracion': proceso.f_elaboracion.strftime('%d/%m/%Y') if proceso.f_elaboracion else "",
            'f_publicacion': proceso.f_publicacion.strftime('%d/%m/%Y') if proceso.f_publicacion else "",
            'f_recepcion': proceso.f_recepcion.strftime('%d/%m/%Y') if proceso.f_recepcion else "",
            'f_cierre': proceso.f_cierre.strftime('%d/%m/%Y') if proceso.f_cierre else "",
            'f_verificacion': proceso.f_verificacion.strftime('%d/%m/%Y') if proceso.f_verificacion else "",
            'f_firma': proceso.f_firma.strftime('%d/%m/%Y') if proceso.f_firma else "",
            'plazo_txt': proceso.plazo_txt,
            'items': items_tabla,
            'total_final': f"${total_acumulado:,.0f}"
        }

        # 5. Escanear Carpeta de Plantillas
        ruta_plantillas = os.path.join(current_app.root_path, 'static', 'plantillas')
        archivos_docs = sorted([f for f in os.listdir(ruta_plantillas) if f.endswith('.docx')])
        
        if not archivos_docs:
            return "No se encontraron plantillas .docx", 404

        ruta_temp = os.path.join(current_app.root_path, 'static', 'temp')
        os.makedirs(ruta_temp, exist_ok=True)

        zip_buffer = BytesIO()
        primer_archivo_generado = None 
        nombre_primer_archivo = ""

        # 5. Escanear y Procesar (Usamos enumerate para el conteo automático)
        with zipfile.ZipFile(zip_buffer, 'w') as zf:
            # enumerate nos da el número (i) empezando en 0
            for i, nombre_p in enumerate(archivos_docs, start=1): 
                doc = DocxTemplate(os.path.join(ruta_plantillas, nombre_p))
                
                # ... (lo de las imágenes se mantiene igual) ...
                if colegio.logo_path:
                    r_logo = os.path.join(current_app.root_path, 'static', 'uploads', colegio.logo_path)
                    if os.path.exists(r_logo):
                        contexto['logo'] = InlineImage(doc, r_logo, width=Mm(40))
                # ... (lo de la firma igual) ...

                doc.render(contexto)
                
                # --- NUEVA LÓGICA DE NOMBRES CON CONTEO ---
                # zfill(2) convierte el 1 en "01", el 2 en "02", etc.
                conteo = str(i).zfill(2)
                
                # Quitamos la extensión .docx del nombre original
                nombre_plantilla_limpio = os.path.splitext(nombre_p)[0].upper()
                
                # Resultado: 01_PLANTILLA_PROCESO_NOMBRECOLEGIO
                nombre_base_final = f"{conteo}_{nombre_plantilla_limpio}_{nombre_col_limpio}"
                
                path_word = os.path.join(ruta_temp, f"{nombre_base_final}.docx")
                doc.save(path_word)

                archivo_a_enviar = path_word
                ext_final = ".docx"

                # Conversión a PDF (se mantiene igual)
                if formato == 'pdf':
                    try:
                        pythoncom.CoInitialize() 
                        path_pdf = path_word.replace(".docx", ".pdf")
                        convert(path_word, path_pdf)
                        archivo_a_enviar = path_pdf
                        ext_final = ".pdf"
                    except Exception as e:
                        print(f"Error PDF: {e}")

                if modo == 'zip':
                    zf.write(archivo_a_enviar, f"{nombre_base_final}{ext_final}")
                else:
                    primer_archivo_generado = archivo_a_enviar
                    nombre_primer_archivo = f"{nombre_base_final}{ext_final}"
                    break 

        # 6. Retorno de archivos
        if modo == 'solo' and primer_archivo_generado:
            return send_file(
                primer_archivo_generado, 
                as_attachment=True,
                download_name=nombre_primer_archivo # Nombre pulido para descarga individual
            )

        zip_buffer.seek(0)
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f"PAQUETE_{nombre_col_limpio}.zip"
        )

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return f"Error técnico: {str(e)}", 500