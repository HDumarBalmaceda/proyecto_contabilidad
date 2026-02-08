// Función para mostrar la vista previa de la imagen seleccionada
function mostrarVistaPrevia(input, previewId, textId) {
  const file = input.files[0];
  const preview = document.getElementById(previewId);
  const text = document.getElementById(textId);

  if (file) {
    const reader = new FileReader();
    reader.onload = function(e) {
      preview.src = e.target.result;       // asignar imagen cargada
      preview.classList.remove("d-none");  // mostrar imagen
      text.classList.add("d-none");        // ocultar texto
    };
    reader.readAsDataURL(file);            // leer archivo como base64
  } else {
    preview.src = "#";                     // limpiar imagen
    preview.classList.add("d-none");       // ocultar imagen
    text.classList.remove("d-none");       // volver a mostrar texto
  }
}

// Asignar eventos a los inputs cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", function() {
  const logoInput = document.getElementById("logo_path");
  const firmaInput = document.getElementById("firma_path");

  if (logoInput) {
    logoInput.addEventListener("change", function() {
      mostrarVistaPrevia(this, "previewLogo", "logoText");
    });
  }

  if (firmaInput) {
    firmaInput.addEventListener("change", function() {
      mostrarVistaPrevia(this, "previewFirma", "firmaText");
    });
  }
});