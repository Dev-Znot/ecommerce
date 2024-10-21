window.addEventListener('resize', function() {
    var formContainer = document.querySelector('.form-container');
    var windowHeight = window.innerHeight;
    formContainer.style.height = windowHeight * 0.8 + 'px'; // Ajuste conforme necessário
});
