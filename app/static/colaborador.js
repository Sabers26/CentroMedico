// Obtén una referencia al select y al elemento que deseas mostrar/ocultar.
const select = document.getElementById('Tipo');
const elemento = document.getElementById('Espe');
const elemento2 = document.getElementById('Espe-l');

// Agrega un evento de cambio al select.
select.addEventListener('change', function() {
  // Obtiene el valor seleccionado en el select.
  const valorSeleccionado = select.value;
  
  // Comprueba el valor seleccionado y ajusta la visibilidad del elemento en consecuencia.
  if (valorSeleccionado === '2') {
    elemento.style.display = 'block'; // Muestra el elemento
    elemento2.style.display = 'block'; // Muestra el elemento
  } else {
    elemento.style.display = 'none'; // Oculta el elemento
    elemento2.style.display = 'none'; // Muestra el elemento
  }
});

function validar() {

  var rutInput = document.getElementById("rut");
  var rut = rutInput.value;

  // Expresión regular que cumple con los requisitos
  var patron = /^[0-9]+[-|‐]{1}[0-9kK]{1}$/;

  // Comprobamos si el RUT cumple con el patrón y la longitud
  if (!patron.test(rut) || rut.length > 10) {
    rutInput.value = ""; // Borra el campo si es inválido
    alert("rut no válido");
    
  }

  var nombreApellidoInput = document.getElementById("nombreApellido");
  var nombreApellido = nombreApellidoInput.value;

  // Expresión regular que cumple con los requisitos
  var patron = /^[A-Za-z ]{1,30}$/;

  // // Comprobamos si el nombre y apellido NO cumplen con el patrón
  // if (!patron.test(nombreApellido)) {
  //   alert("Nombre y apellido no válidos");
  //   nombreApellidoInput.value = ""; // Borra el campo si es inválido
  // }

};

