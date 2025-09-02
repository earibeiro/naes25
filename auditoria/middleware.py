"""
Middleware para capturar informações da requisição e disponibilizar
globalmente via thread-local storage
"""
from .local import set_current_request, clear_current_request


class RequestStoreMiddleware:
    """
    Middleware que armazena a requisição atual em thread-local
    para ser acessada pelos signals de auditoria
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Armazena a requisição no thread-local
        set_current_request(request)
        
        try:
            # Processa a requisição
            response = self.get_response(request)
            return response
        finally:
            # Limpa o thread-local após processar
            clear_current_request()