from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Inicializamos las extensiones
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.secret_key = 'mi_llave_secreta_super_segura_123'

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Importar modelos
        from app.modelos import models 
        
        # 1. Registro Colegios
        from app.controladores.colegios.form_colegios_controlador import colegios_bp
        app.register_blueprint(colegios_bp)

        # 2. Registro Proveedores
        from app.controladores.proveedores.proveedores_controlador import proveedores_bp
        app.register_blueprint(proveedores_bp)

       # 3. REGISTRO PROCESOS
        try:
            from app.controladores.perfil_colegios.procesos_controlador import procesos_bp
            app.register_blueprint(procesos_bp, url_prefix='/procesos')
            print("✅ Blueprint de procesos cargado correctamente")
        except Exception as e:
            print(f"❌ ERROR al cargar controlador de procesos: {e}")
            
        except (ImportError, ModuleNotFoundError):
            try:
                # Intento alternativo si realmente está dentro de 'colegios'
                from app.controladores.colegios.perfil_colegios.procesos_controlador import procesos_bp
                app.register_blueprint(procesos_bp, url_prefix='/procesos')
                print("✅ Blueprint de procesos registrado (Ruta larga)")
            except Exception as e:
                print(f"❌ ERROR CRÍTICO: No se encontró el archivo procesos_controlador.py: {e}")

    @app.route("/")
    def index():
        from flask import redirect, url_for
        return redirect(url_for('colegios.mostrar_colegios'))

    return app