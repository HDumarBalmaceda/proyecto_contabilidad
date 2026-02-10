# -------------------------
# Importar la instancia de db desde app/__init__.py
# -------------------------
from app import db

# -------------------------
# Modelo: Colegio
# Representa la tabla 'colegios' en la base de datos
# -------------------------
class Colegio(db.Model):
    __tablename__ = 'colegios'

    # Clave primaria
    id = db.Column(db.Integer, primary_key=True)

    # Datos básicos del colegio
    nombre = db.Column(db.String(200), nullable=False)
    nit = db.Column(db.String(50), unique=True)
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(50))
    municipio = db.Column(db.String(100))

    # Información del rector
    rector_nombre = db.Column(db.String(150))
    rector_documento = db.Column(db.String(50))
    rector_tipo_documento = db.Column(
        db.Enum('CC', 'CE', 'TI', 'PAS', 'OTRO', name='doc_type', create_type=False),
        nullable=False,
        default='CC'
    )

    # Rutas de archivos (logo y firma)
    logo_path = db.Column(db.String(500))
    firma_path = db.Column(db.String(500))

    # Timestamps automáticos
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())

    # Representación en consola
    def __repr__(self):
        return f"<Colegio {self.nombre}>"