// Obtén una referencia al select y al elemento que deseas mostrar/ocultar.
const select = document.getElementById('Tipo');
const elemento = document.getElementById('Espe');
const elemento2 = document.getElementById('Espe-l');

// Agrega un evento de cambio al select.
select.addEventListener('change', function() {
  // Obtiene el valor seleccionado en el select.
  const valorSeleccionado = select.value;
  
  // Comprueba el valor seleccionado y ajusta la visibilidad del elemento en consecuencia.
  if (valorSeleccionado === '1') {
    elemento.style.display = 'block'; // Muestra el elemento
    elemento2.style.display = 'block'; // Muestra el elemento
  } else {
    elemento.style.display = 'none'; // Oculta el elemento
    elemento2.style.display = 'none'; // Muestra el elemento
  }
});