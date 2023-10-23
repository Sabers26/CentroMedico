// Obtén una referencia al select y al elemento que deseas mostrar/ocultar.
const select = document.getElementById('tipo');
const elemento = document.getElementById('espe');

// Agrega un evento de cambio al select.
select.addEventListener('change', function() {
  // Obtiene el valor seleccionado en el select.
  const valorSeleccionado = select.value;
  
  // Comprueba el valor seleccionado y ajusta la visibilidad del elemento en consecuencia.
  if (valorSeleccionado === '2') {
    elemento.style.display = 'block'; // Muestra el elemento
    elemento.style.marginLeft = '40%';
    elemento.style.marginTop = '2%';
    elemento.style.marginBottom = '2%';
  } else {
    elemento.style.display = 'none'; // Oculta el elemento
    var selectElement = document.getElementById("espe");
  
    // Establece el índice de la opción que deseas seleccionar
    selectElement.selectedIndex = null; // Esto seleccionará la "Opción 3"
  }
});
