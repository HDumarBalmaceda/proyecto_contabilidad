function abrirHistorial(colegioId) {
    const modalElement = document.getElementById('modalHistorial');
    const myModal = new bootstrap.Modal(modalElement);
    const contenedor = document.getElementById('contenedorHistorial');

    contenedor.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2 text-muted small">Buscando expedientes históricos...</p>
        </div>`;

    myModal.show();

    fetch(`/historial/historial_json/${colegioId}`)
        .then(response => {
            if (!response.ok) throw new Error('Error en la red');
            return response.json();
        })
        .then(data => {
            if (!data || data.length === 0) {
                contenedor.innerHTML = `
                    <div class="text-center py-5">
                        <i class="bi bi-folder2-open display-4 text-muted opacity-50"></i>
                        <p class="text-muted mt-3">No se encontraron procesos previos.</p>
                    </div>`;
                return;
            }

            // --- INICIO DE LA CUADRÍCULA ---
            // Usamos row-cols para definir cuántas tarjetas por fila (1 en móvil, 2 en tablet, 3 en pc)
         // ... (dentro del .then(data =>))

let html = '<div class="list-group list-group-flush border-top">';

// Usamos index para enumerar (el +1 es porque empieza en 0)
data.forEach((proceso, index) => {
    html += `
    <div class="list-group-item list-group-item-action py-3 px-4 border-bottom">
        <div class="row align-items-center">
            <div class="col-auto text-center border-end pe-4" style="min-width: 120px;">
                <div class="fw-bold text-primary h5 mb-0">${proceso.vigencia}</div>
                <div class="badge bg-secondary-subtle text-secondary border small">PROCESO #${index + 1}</div>
            </div>

            <div class="col ms-2">
                <div class="d-flex align-items-center mb-1">
                    <i class="bi bi-briefcase text-secondary me-2"></i>
                    <h6 class="mb-0 text-uppercase fw-bold text-dark" style="font-size: 0.9rem;">
                        ${proceso.tipo_contrato} 
                    </h6>
                    <span class="ms-2 text-muted small fw-normal">| ID: ${proceso.id}</span>
                </div>
                <div class="text-muted small">
                    <i class="bi bi-person-check-fill me-1 text-success"></i> 
                    <strong>CONTRATISTA:</strong> ${proceso.proveedor}
                </div>
            </div>

            <div class="col-auto">
                <div class="d-flex gap-2">
                    <a href="/reportes/descargar_zip/${proceso.id}?formato=pdf" 
   class="btn btn-sm btn-primary d-flex align-items-center px-3 shadow-sm" 
   title="Descargar todos los documentos en ZIP">
    <i class="bi bi-cloud-arrow-down-fill me-1"></i> DESCARGAR EXPEDIENTE
</a>
                    <button onclick="verDetalleProceso(${proceso.id})" 
                            class="btn btn-sm btn-outline-secondary px-3" 
                            title="Ver detalles">
                        <i class="bi bi-eye"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>`;
});

html += '</div>';
contenedor.innerHTML = html;

            html += '</div>'; // Cerramos el row
            contenedor.innerHTML = html;
        })
        .catch(error => {
            console.error('Error:', error);
            contenedor.innerHTML = `<div class="alert alert-danger m-3 small">Error al cargar historial.</div>`;
        });
}