from django.urls import path
from .views import MainPage, AboutView, ProjectsView, ContactView
from .views import StateCreateView, CityCreateView, PersonCreateView, CompanyCreateView
from .views import StateUpdateView, CityUpdateView, PersonUpdateView, CompanyUpdateView
from .views import StateDeleteView, CityDeleteView, PersonDeleteView, CompanyDeleteView

urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('create/state/', StateCreateView.as_view(), name='create-state'),
    path('create/city/', CityCreateView.as_view(), name='create-city'),
    path('create/person/', PersonCreateView.as_view(), name='form_person'),
    path('create/company/', CompanyCreateView.as_view(), name='form_company'),
    path('update/state/<int:pk>/', StateUpdateView.as_view(), name='update-state'),
    path('update/city/<int:pk>/', CityUpdateView.as_view(), name='update-city'),
    path('update/person/<int:pk>/', PersonUpdateView.as_view(), name='update-person'),
    path('update/company/<int:pk>/', CompanyUpdateView.as_view(), name='update-company'),
    path('delete/state/<int:pk>/', StateDeleteView.as_view(), name='delete-state'),
    path('delete/city/<int:pk>/', CityDeleteView.as_view(), name='delete-city'),
    path('delete/person/<int:pk>/', PersonDeleteView.as_view(), name='delete-person'),
    path('delete/company/<int:pk>/', CompanyDeleteView.as_view(), name='delete-company'),
    #path('endereço/', MinhaView.as_view(), name='nome-da-url'),
]
