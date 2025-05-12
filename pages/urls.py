from django.urls import path
from .views import MainPage, AboutView

urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    #path('endereço/', MinhaView.as_view(), name='nome-da-url'),
]
