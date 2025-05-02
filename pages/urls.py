from django.urls import path
from .views import MainPage

urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    #path('endereço/', MinhaView.as_view(), name='nome-da-url'),
]
