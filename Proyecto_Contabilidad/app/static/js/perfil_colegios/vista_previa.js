function abrirVistaPrevia() {
    // 1. Capturar datos de los inputs del formulario
    const form = document.getElementById('formExpedienteCompleto');
    
    // Obtenemos los valores de los inputs por su atributo 'name'
    const objeto = form.querySelector('[name="objeto_desc"]').value;
    const cdp = form.querySelector('[name="cdp_numero"]').value;
    const vigencia = document.getElementById('modalVigenciaInput').value;
    
    // Obtener nombre del proveedor seleccionado
    const selectProv = form.querySelector('[name="proveedor_id"]');
    const proveedorNombre = selectProv.options[selectProv.selectedIndex].text;

    // 2. Llenar los textos en el modal de Vista Previa
    document.getElementById('vp_objeto').innerText = objeto || "(No definido)";
    document.getElementById('vp_cdp').innerText = cdp || "____";
    document.getElementById('vp_vigencia').innerText = vigencia;
    document.getElementById('vp_proveedor').innerText = proveedorNombre;

    // 3. Cargar datos del colegio (desde las variables globales que pusimos en el HTML)
    document.getElementById('vp_colegio_nombre').innerText = window.datosColegio.nombre.toUpperCase();
    document.getElementById('vp_colegio_nit').innerText = window.datosColegio.nit;
    document.getElementById('vp_rector_nombre').innerText = window.datosColegio.rector;
    
    // Cargar imágenes
    if(window.datosColegio.logo) document.getElementById('vp_logo').src = window.datosColegio.logo;
    if(window.datosColegio.firma) document.getElementById('vp_firma').src = window.datosColegio.firma;

    // 4. Procesar la tabla de ítems
    dibujarTablaEnPrevia();

    // 5. Abrir el modal de vista previa
    const modalPrevia = new bootstrap.Modal(document.getElementById('modalVistaPrevia'));
    modalPrevia.show();
}

function dibujarTablaEnPrevia() {
    const filas = document.querySelectorAll('#cuerpoTablaItems tr');
    let html = `
        <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
            <thead>
                <tr style="background: #eee;">
                    <th style="border: 1px solid #000; padding: 4px;">Cant.</th>
                    <th style="border: 1px solid #000; padding: 4px;">Descripción</th>
                    <th style="border: 1px solid #000; padding: 4px;">Total</th>
                </tr>
            </thead>
            <tbody>`;

    filas.forEach(fila => {
        const cant = fila.querySelector('[name="cant[]"]').value;
        const desc = fila.querySelector('[name="desc[]"]').value;
        const total = fila.querySelector('[name="v_total[]"]').value;

        if(desc.trim() !== "") {
            html += `
                <tr>
                    <td style="border: 1px solid #000; padding: 4px; text-align: center;">${cant}</td>
                    <td style="border: 1px solid #000; padding: 4px;">${desc}</td>
                    <td style="border: 1px solid #000; padding: 4px; text-align: right;">$${parseFloat(total).toLocaleString()}</td>
                </tr>`;
        }
    });

    html += `</tbody></table>`;
    document.getElementById('vp_tabla_items').innerHTML = html;
}