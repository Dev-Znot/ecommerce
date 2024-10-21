const bar = document.getElementById('bar');
const close = document.getElementById('close');
const nav = document.getElementById('navbar');

if (bar) {
    bar.addEventListener('click', () => {
        nav.classList.add('active');
    })
}
if (close) {
    close.addEventListener('click', () => {
        nav.classList.remove('active');
    })
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

$(document).ready(function() {
    $('.cartSend').click(function() {
        var pk = $(this).data('pk');
        var csrftoken = getCookie('csrftoken'); 
        $.ajax({
        url: '/cart/',  // Inclui a URL
        type: 'POST',
        data:JSON.stringify({pk:pk}), // Pro corpo
        contentType:'aplication/json',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken); // Define o cabeçalho CSRF
        },
        success: function(result) {
            location.reload();
            console.log('Adicionado ao carrinho');
            // Aqui você pode atualizar a página ou fazer outra ação após a exclusão
        },
        error: function(xhr, status, error) {
            console.error('Erro ao Adicionar objeto:', error);
        }
        });
    });
});   











