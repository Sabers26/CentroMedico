// Obtén una referencia al select y al elemento que deseas mostrar/ocultar.
function mostrarSelect(valorSeleccionado) {
  var selectSecundario = document.getElementById('espe');
  var label = document.getElementById('espe-l');
  if (valorSeleccionado == '2') {
      selectSecundario.style.display = 'block';
      selectSecundario.style.marginLeft = '25%';
      label.style.display = 'block';
      label.style.marginLeft = '1%';
  } else {
      selectSecundario.style.display = 'none';
      label.style.display = 'none';
  }
}

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

