"""
Thread-local storage para capturar informações da requisição atual
"""
import threading

# Storage thread-local para a requisição atual
_local = threading.local()


def set_current_request(request):
    """Define a requisição atual no thread-local"""
    _local.request = request


def get_current_request():
    """Obtém a requisição atual do thread-local"""
    return getattr(_local, "request", None)


def clear_current_request():
    """Limpa a requisição atual do thread-local"""
    if hasattr(_local, "request"):
        del _local.request