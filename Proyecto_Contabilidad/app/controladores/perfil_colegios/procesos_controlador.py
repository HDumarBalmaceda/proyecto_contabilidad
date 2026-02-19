from flask import Blueprint, request, jsonify
from app import db
from app.modelos.models import ProcesoContractual, ItemProceso  # Ajusta la ruta a tus modelos
from datetime import datetime

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