/**
 * exportar_documentos.js
 * Maneja la interfaz de SweetAlert2 para elegir formato y modo.
 */

function abrirOpcionesDescarga(datosParaEnviar, colegioId) {
    Swal.fire({
        title: 'Finalizar Expediente',
        html: `
            <div class="text-start mt-2">
                <label class="form-label fw-bold small">1. Seleccione Formato</label>
                <select id="swal-formato" class="form-select mb-3">
                    <option value="word">Microsoft Word (.docx)</option>
                    <option value="pdf">Documento PDF (.pdf)</option>
                </select>

                <label class="form-label fw-bold small">2. Seleccione Modo</label>
                <select id="swal-modo" class="form-select">
                    <option value="zip">Paquete Completo (ZIP)</option>
                    <option value="solo">Descargar independientemente</option>
                </select>
            </div>
        `,
        icon: 'info',
        showCancelButton: true,
        confirmButtonText: 'Generar y Descargar',
        confirmButtonColor: '#198754',
        preConfirm: () => {
            return {
                formato: document.getElementById('swal-formato').value,
                modo: document.getElementById('swal-modo').value
            }
        }
    }).then((result) => {
        if (result.isConfirmed) {
            ejecutarEnvioFinal(datosParaEnviar, colegioId, result.value);
        }
    });
}

async function ejecutarEnvioFinal(datos, colegioId, opciones) {
    Swal.fire({
        title: 'Generando Documentos...',
        text: 'Estamos preparando tus archivos. Por favor, no cierres esta ventana.',
        allowOutsideClick: false,
        didOpen: () => { Swal.showLoading(); }
    });

    try {
        const response = await fetch(`/procesos/guardar_proceso/${colegioId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        const resultado = await response.json();

        if (resultado.status === 'success') {
            const urlDescarga = `/procesos/descargar_documentos/${resultado.proceso_id}?formato=${opciones.formato}&modo=${opciones.modo}`;
            
            // 1. Iniciamos la descarga
            window.location.href = urlDescarga;

            // 2. Cambiamos la alerta a modo "Listo" pero sin cerrar ni recargar
            Swal.fire({
                icon: 'success',
                title: '¡Proceso Iniciado!',
                html: `
                    <div class="text-center">
                        <p>Los archivos se están enviando a tu carpeta de descargas.</p>
                        <p class="text-muted small">Si la descarga no inicia en unos segundos, revisa que no tengas bloqueadores de ventanas emergentes.</p>
                        <hr>
                        <button type="button" class="btn btn-primary" onclick="location.reload()">
                            Finalizar
                        </button>
                    </div>
                `,
                showConfirmButton: false, // Quitamos el botón de SweetAlert por defecto
                allowOutsideClick: false  // Obligamos a usar nuestro botón de recarga
            });

        } else {
            Swal.fire('Error', resultado.message, 'error');
        }
    } catch (error) {
        console.error("Error:", error);
        Swal.fire('Error', 'No se pudo conectar con el servidor', 'error');
    }
}