from flask import Blueprint, render_template, request, redirect, url_for, flash

# Definimos el blueprint con el nombre 'proveedores'
# El url_prefix='/proveedores' hará que todas las rutas de este archivo empiecen así
proveedores_bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')

@proveedores_bp.route('/')
def listar_proveedores():
    """
    Esta función se encarga de mostrar la tabla de proveedores.
    Es la que responde al url_for('proveedores.listar_proveedores')
    """
    # Por ahora, como no tenemos base de datos de proveedores aún, 
    # pasamos una lista vacía o simplemente renderizamos.
    # Cuando tengas el modelo listo, aquí harás: proveedores = Proveedor.query.all()
    return render_template('proveedores/proveedores.html')

# --- Aquí irán las rutas del CRUD más adelante ---

# @proveedores_bp.route('/crear', methods=['POST'])
# def crear_proveedor():
#     pass