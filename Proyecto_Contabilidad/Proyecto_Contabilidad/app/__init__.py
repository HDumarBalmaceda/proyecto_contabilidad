from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Inicializamos las extensiones fuera de la factoría
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Cifra la información enviada 
    app.secret_key = 'mi_llave_secreta_super_segura_123'

    # Inicializar db y migrate con la app
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Importar modelos para que SQLAlchemy cree las tablas
        from app.modelos import models 
        
        # 1. Registro del Blueprint de Colegios
        from app.controladores.colegios.form_colegios_controlador import colegios_bp
        app.register_blueprint(colegios_bp)

        # 2. REGISTRO DEL BLUEPRINT DE PROVEEDORES (AQUÍ ESTÁ LA MAGIA)
        from app.controladores.proveedores.proveedores_controlador import proveedores_bp
        app.register_blueprint(proveedores_bp)

    @app.route("/")
    def index():
        # Tip: Podrías hacer que la raíz te redirija directamente a colegios
        from flask import redirect, url_for
        return redirect(url_for('colegios.mostrar_colegios'))

    return app