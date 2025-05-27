from django.urls import path
from .views import MainPage, AboutView, ProjectsView, ContactView

urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('contact/', ContactView.as_view(), name='contact'),
    #path('endereço/', MinhaView.as_view(), name='nome-da-url'),
]
