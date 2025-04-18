from django.urls import path
from .views import IndexView

urlpatterns = [
    path('inicio/', IndexView.as_view(), name='inicio'),
    #path('endereço/', MinhaView.as_view(), name='nome-da-url'),
]
