# -------------------------
# Controlador: Colegios
# -------------------------
import os
from flask import Blueprint, request, redirect, url_for, flash, render_template
from app import db
from app.modelos.models import Colegio

# Crear blueprint para colegios
colegios_bp = Blueprint('colegios', __name__, url_prefix='/colegios')

# 1. RUTA PARA MOSTRAR LA PÁGINA PRINCIPAL (colegios.html)
@colegios_bp.route('/')
def mostrar_colegios():
    # Consultamos los colegios para que se puedan listar después
    colegios = Colegio.query.all()
    return render_template('colegios/colegios.html', colegios=colegios)

# 2. RUTA PARA CREAR COLEGIO (POST)
@colegios_bp.route('/crear', methods=['POST'])
def crear_colegio():
    try:
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        nit = request.form.get('nit')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        municipio = request.form.get('municipio')
        rector_nombre = request.form.get('rector_nombre')
        rector_documento = request.form.get('rector_documento')
        rector_tipo_documento = request.form.get('rector_tipo_documento')

        # Manejo de archivos (logo y firma)
        logo_file = request.files.get('logo_path')
        firma_file = request.files.get('firma_path')

        logo_filename = None
        firma_filename = None

        # Asegúrate de que esta carpeta exista: app/static/uploads
        upload_folder = os.path.join("app", "static", "uploads")
        
        # Crear la carpeta si no existe para evitar errores
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        if logo_file and logo_file.filename != '':
            logo_filename = f"logo_{nombre.replace(' ', '_')}.png"
            logo_file.save(os.path.join(upload_folder, logo_filename))

        if firma_file and firma_file.filename != '':
            firma_filename = f"firma_{nombre.replace(' ', '_')}.png"
            firma_file.save(os.path.join(upload_folder, firma_filename))

        # Crear objeto Colegio
        nuevo_colegio = Colegio(
            nombre=nombre,
            nit=nit,
            direccion=direccion,
            telefono=telefono,
            municipio=municipio,
            rector_nombre=rector_nombre,
            rector_documento=rector_documento,
            rector_tipo_documento=rector_tipo_documento,
            logo_path=logo_filename,
            firma_path=firma_filename
        )

        # Guardar en la base de datos
        db.session.add(nuevo_colegio)
        db.session.commit()

        flash("Colegio creado exitosamente ✅", "success")
        # Redirige a la función 'mostrar_colegios' de este mismo blueprint
        return redirect(url_for('colegios.mostrar_colegios'))

    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear colegio: {str(e)}", "danger")
        return redirect(url_for('colegios.mostrar_colegios'))

        # Añade esto al final de form_colegios_controlador.py

@colegios_bp.route('/<int:id>')
def detalle_colegio(id):
    # Buscamos el colegio por su ID o devolvemos un error 404 si no existe
    colegio = Colegio.query.get_or_404(id)
    
    # Por ahora, vamos a renderizar una página que crearemos en el siguiente paso
    return render_template('colegios/perfil_colegio.html', colegio=colegio)