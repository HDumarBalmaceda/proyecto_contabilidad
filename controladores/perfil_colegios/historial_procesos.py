from flask import Blueprint, jsonify
from app.modelos.models import ProcesoContractual, Proveedor
from app import db

# Crear un blueprint separado para procesos si así lo deseas
historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial_json/<int:colegio_id>')
def historial_json(colegio_id):
    try:
        # Consultamos los procesos usando el modelo ProcesoContractual
        # Cargamos el proveedor relacionado para evitar consultas extra (joinedload)
        procesos = ProcesoContractual.query.filter_by(colegio_id=colegio_id)\
                   .order_by(ProcesoContractual.id.desc()).all()
        
        resultado = []
        for p in procesos:
            # Determinamos el nombre del proveedor
            # p.colegio.proveedores no funcionaría igual que p.proveedor_id
            # Buscamos el proveedor directamente por su ID asociado al proceso
            prov = Proveedor.query.get(p.proveedor_id)
            if prov:
                nombre_prov = prov.razon_social if prov.razon_social else f"{prov.primer_nombre} {prov.primer_apellido}"
            else:
                nombre_prov = "No asignado"

            resultado.append({
                 'id': p.id,
                 'vigencia': p.vigencia,
                 'tipo_contrato': p.tipo_contrato,  # <--- Faltaba el : y la ,
                 'objeto_corto': (p.objeto_desc[:85] + '...') if p.objeto_desc and len(p.objeto_desc) > 85 else p.objeto_desc,
                 'proveedor': nombre_prov.strip()
             })
        
        return jsonify(resultado)

    except Exception as e:
        print(f"Error en historial: {str(e)}")
        return jsonify([]), 500