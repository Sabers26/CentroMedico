document.addEventListener('DOMContentLoaded', function() {
  const dato = document.getElementById('tipo');
  const select = dato.getAttribute('data-mi-valor');
  console.log("prueba si llegue aqui")
  console.log(select)


  const elemento = document.getElementById('espe');

  const valorSeleccionado = select;
  
  // Comprueba el valor seleccionado y ajusta la visibilidad del elemento en consecuencia.
  if (valorSeleccionado === '2') {
    elemento.style.display = 'block'; // Muestra el elemento
    elemento.style.marginLeft = '5%';
    elemento.style.marginTop = '2%';
    elemento.style.marginBottom = '2%';
  } else {
    elemento.style.display = 'none'; // Oculta el elemento
    var selectElement = document.getElementById("espe");
  
    // Establece el índice de la opción que deseas seleccionar
    selectElement.selectedIndex = null; 
  }
});
