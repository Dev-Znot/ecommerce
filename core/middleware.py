from django.utils.functional import SimpleLazyObject
from django.contrib.sessions.middleware import SessionMiddleware

# Middleware para inicializar a sessão do usuario em cada requisição

class InitializeSessionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.save()
        return self.get_response(request)

# Definindo valores para sessão

def set_session(request):

    if "cart" not in request.session:
        request.session['cart'] = []
    
    if "whislist" not in request.session:
        request.session['whislist'] = []


class CartMiddleware(SessionMiddleware):
    
    def process_request(self, request):
        super().process_request(request)
        request.quantidade_itens_carrinho = SimpleLazyObject(lambda: self.get_quantidade_itens_carrinho(request))

    def get_quantidade_itens_carrinho(self, request):
        carinho_de_compras = request.session.get('cart', [])
        return len(carinho_de_compras)
