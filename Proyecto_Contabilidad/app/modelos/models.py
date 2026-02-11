from app import db

# 1. TABLA INTERMEDIA (Asociación Muchos a Muchos)
# Se coloca fuera de las clases porque es una tabla de soporte
colegio_proveedor = db.Table('colegio_proveedor',
    db.Column('colegio_id', db.Integer, db.ForeignKey('colegios.id'), primary_key=True),
    db.Column('proveedor_id', db.Integer, db.ForeignKey('proveedores.id'), primary_key=True)
)

# -------------------------
# Modelo: Colegio
# -------------------------
class Colegio(db.Model):
    __tablename__ = 'colegios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    nit = db.Column(db.String(50), unique=True)
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(50))
    municipio = db.Column(db.String(100))
    rector_nombre = db.Column(db.String(150))
    rector_documento = db.Column(db.String(50))
    rector_tipo_documento = db.Column(
        db.Enum('CC', 'CE', 'TI', 'PAS', 'OTRO', name='doc_type', create_type=False),
        nullable=False,
        default='CC'
    )
    logo_path = db.Column(db.String(500))
    firma_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())

    # --- NUEVA LÍNEA: Relación con Proveedores ---
    proveedores = db.relationship('Proveedor', secondary=colegio_proveedor, backref='colegios_vinculados')

    def __repr__(self):
        return f"<Colegio {self.nombre}>"

# -------------------------
# Modelo: Proveedor
# -------------------------
class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    tipo_tercero = db.Column(db.String(50), nullable=False)
    documento = db.Column(db.String(20), unique=True, nullable=False)
    dv = db.Column(db.String(1))
    renta = db.Column(db.String(50))
    primer_nombre = db.Column(db.String(100))
    segundo_nombre = db.Column(db.String(100))
    primer_apellido = db.Column(db.String(100))
    segundo_apellido = db.Column(db.String(100))
    razon_social = db.Column(db.String(255))
    direccion = db.Column(db.String(255))
    departamento = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    movil = db.Column(db.String(50))
    correo_electronico = db.Column(db.String(150))
    banco = db.Column(db.String(100))
    no_cuenta = db.Column(db.String(50))
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        nombre = self.razon_social if self.razon_social else f"{self.primer_nombre} {self.primer_apellido}"
        return f'<Proveedor {nombre}>'