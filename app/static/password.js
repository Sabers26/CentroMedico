document.addEventListener('DOMContentLoaded', function() {
    var passwordInput = document.getElementById('Password');
    var confirmPasswordInput = document.getElementById('password2');
    var form = document.getElementById('registro-form');

    function validatePassword() {
        if (passwordInput.value !== confirmPasswordInput.value) {
            alert('Las contraseñas no coinciden. Por favor, inténtalo de nuevo.');
            confirmPasswordInput.focus();
            return false;
        }
        return true;
    }

    form.addEventListener('submit', function(event) {
        if (!validatePassword()) {
            event.preventDefault(); // Evita el envío del formulario si las contraseñas no coinciden
        }
    });


    
});



