from django.urls import path
from .views import (
    HomeView,  # IMPORTAR HomeView
    AboutView, ProjectsView, ContactView,
    StateCreateView, CityCreateView, PersonCreateView, CompanyCreateView,
    StateUpdateView, CityUpdateView, PersonUpdateView, CompanyUpdateView,
    StateDeleteView, CityDeleteView, PersonDeleteView, CompanyDeleteView,
    StateListView, CityListView, PersonListView, CompanyListView,
    StateDetailView, CityDetailView, PersonDetailView, CompanyDetailView
)

urlpatterns = [
    # USAR HomeView na URL principal
    path('', HomeView.as_view(), name='home'),
    path('index/', HomeView.as_view(), name='index'),  # Compatibilidade
    
    path('about/', AboutView.as_view(), name='about'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('contact/', ContactView.as_view(), name='contact'),
    
    # CRUD States
    path('states/', StateListView.as_view(), name='state-list'),
    path('states/<int:pk>/', StateDetailView.as_view(), name='state-detail'),
    path('create/state/', StateCreateView.as_view(), name='create-state'),
    path('update/state/<int:pk>/', StateUpdateView.as_view(), name='update-state'),
    path('delete/state/<int:pk>/', StateDeleteView.as_view(), name='delete-state'),
    
    # CRUD Cities
    path('cities/', CityListView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetailView.as_view(), name='city-detail'),
    path('create/city/', CityCreateView.as_view(), name='create-city'),
    path('update/city/<int:pk>/', CityUpdateView.as_view(), name='update-city'),
    path('delete/city/<int:pk>/', CityDeleteView.as_view(), name='delete-city'),
    
    # CRUD Persons
    path('persons/', PersonListView.as_view(), name='person-list'),
    path('persons/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('create/person/', PersonCreateView.as_view(), name='create-person'),
    path('update/person/<int:pk>/', PersonUpdateView.as_view(), name='update-person'),
    path('delete/person/<int:pk>/', PersonDeleteView.as_view(), name='delete-person'),
    
    # CRUD Companies
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('create/company/', CompanyCreateView.as_view(), name='create-company'),
    path('update/company/<int:pk>/', CompanyUpdateView.as_view(), name='update-company'),
    path('delete/company/<int:pk>/', CompanyDeleteView.as_view(), name='delete-company'),
]
