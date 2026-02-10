import os
from flask import Blueprint, request, render_template, url_for
from app import db
from app.modelos.models import Colegio

# Crear blueprint para colegios
colegios_bp = Blueprint('colegios', __name__, url_prefix='/colegios')

# 1. RUTA PARA MOSTRAR LA PÁGINA PRINCIPAL
@colegios_bp.route('/')
def mostrar_colegios():
    colegios = Colegio.query.all()
    return render_template('colegios/colegios.html', colegios=colegios)

# 2. RUTA PARA CREAR COLEGIO (AJAX para SweetAlert)
@colegios_bp.route('/crear', methods=['POST'])
def crear_colegio():
    try:
        nombre = request.form.get('nombre')
        # ... (captura de los demás campos igual que antes)
        nit = request.form.get('nit')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        municipio = request.form.get('municipio')
        rector_nombre = request.form.get('rector_nombre')
        rector_documento = request.form.get('rector_documento')
        rector_tipo_documento = request.form.get('rector_tipo_documento')

        # Manejo de archivos
        logo_file = request.files.get('logo_path')
        firma_file = request.files.get('firma_path')
        upload_folder = os.path.join("app", "static", "uploads")
        
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        logo_filename = f"logo_{nombre.replace(' ', '_')}.png" if logo_file else None
        if logo_file: logo_file.save(os.path.join(upload_folder, logo_filename))

        firma_filename = f"firma_{nombre.replace(' ', '_')}.png" if firma_file else None
        if firma_file: firma_file.save(os.path.join(upload_folder, firma_filename))

        nuevo_colegio = Colegio(
            nombre=nombre, nit=nit, direccion=direccion, telefono=telefono,
            municipio=municipio, rector_nombre=rector_nombre,
            rector_documento=rector_documento, rector_tipo_documento=rector_tipo_documento,
            logo_path=logo_filename, firma_path=firma_filename
        )

        db.session.add(nuevo_colegio)
        db.session.commit()

        # RESPUESTA PARA EL FETCH DE JS
        return {"status": "success", "message": "Colegio creado"}, 200

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}, 500

# 3. RUTA PARA EL DETALLE (ID único)
@colegios_bp.route('/<int:id>')
def detalle_colegio(id):
    colegio = Colegio.query.get_or_404(id)
    return render_template('perfil_colegios/perfil_colegio.html', colegio=colegio)

#ruta para editar la informacion de los colegios
@colegios_bp.route('/editar/<int:id>', methods=['POST'])
def editar_colegio(id):
    try:
        colegio = Colegio.query.get_or_404(id)
        upload_folder = os.path.join("app", "static", "uploads")

        # Actualizamos los campos de texto
        colegio.nombre = request.form.get('nombre')
        colegio.nit = request.form.get('nit')
        colegio.direccion = request.form.get('direccion')
        colegio.telefono = request.form.get('telefono')
        colegio.municipio = request.form.get('municipio')
        colegio.rector_nombre = request.form.get('rector_nombre')
        colegio.rector_documento = request.form.get('rector_documento')
        colegio.rector_tipo_documento = request.form.get('rector_tipo_documento')

        # Procesar nuevo Logo (solo si se subió uno)
        logo_file = request.files.get('logo_path')
        if logo_file and logo_file.filename != '':
            logo_filename = f"logo_{id}_{colegio.nombre.replace(' ', '_')}.png"
            logo_file.save(os.path.join(upload_folder, logo_filename))
            colegio.logo_path = logo_filename

        # Procesar nueva Firma (solo si se subió una)
        firma_file = request.files.get('firma_path')
        if firma_file and firma_file.filename != '':
            firma_filename = f"firma_{id}_{colegio.nombre.replace(' ', '_')}.png"
            firma_file.save(os.path.join(upload_folder, firma_filename))
            colegio.firma_path = firma_filename

        db.session.commit()
        return {"status": "success", "message": "Información actualizada correctamente"}, 200

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}, 500

    
#funcion para eliminar los  colegios
@colegios_bp.route('/eliminar/<int:id>', methods=['DELETE'])
def eliminar_colegio(id):
    try:
        colegio = Colegio.query.get_or_404(id)
        
        # Opcional: Borrar los archivos físicos del servidor para no llenar espacio
        upload_folder = os.path.join("app", "static", "uploads")
        for archivo in [colegio.logo_path, colegio.firma_path]:
            if archivo:
                ruta_fisica = os.path.join(upload_folder, archivo)
                if os.path.exists(ruta_fisica):
                    os.remove(ruta_fisica)

        db.session.delete(colegio)
        db.session.commit()
        return {"status": "success", "message": "Colegio eliminado definitivamente"}, 200

    except Exception as e:
        db.session.rollback()
        return {"status": "error", "message": str(e)}, 500