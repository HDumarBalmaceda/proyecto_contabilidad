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
    

    # cifra la informacion enviada 
    app.secret_key = 'mi_llave_secreta_super_segura_123'

    # Inicializar db y migrate con la app
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Importar modelos para que SQLAlchemy cree las tablas
        from app.modelos import models 
        
        # Importar y registrar el Blueprint AQUÍ ADENTRO
        from app.controladores.colegios.form_colegios_controlador import colegios_bp
        app.register_blueprint(colegios_bp)

    @app.route("/")
    def index():
        return "Servidor Flask funcionando correctamente ✅"

    return app