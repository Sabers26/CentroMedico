function redireccionar() {
    var selectElement = document.getElementById("admin");
    var selectedOption = selectElement.options[selectElement.selectedIndex];

    // Verifica si se ha seleccionado una opción válida antes de redirigir
    if (selectedOption.value) {
        window.location.href = selectedOption.value;
    }
}