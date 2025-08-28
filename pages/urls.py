from django.urls import path
from . import views

urlpatterns = [
    # Páginas principais
    path('', views.IndexView.as_view(), name='index'),
    path('sobre/', views.AboutView.as_view(), name='about'),
    path('dashboard/', views.HomeView.as_view(), name='home'),
    
    # Person URLs
    path('pessoas/', views.PersonListView.as_view(), name='person-list'),
    path('pessoas/nova/', views.PersonCreateView.as_view(), name='create-person'),
    path('pessoas/<int:pk>/', views.PersonDetailView.as_view(), name='detail-person'),
    path('pessoas/<int:pk>/editar/', views.PersonUpdateView.as_view(), name='update-person'),
    path('pessoas/<int:pk>/excluir/', views.PersonDeleteView.as_view(), name='delete-person'),
    
    # Company URLs
    path('empresas/', views.CompanyListView.as_view(), name='company-list'),
    path('empresas/nova/', views.CompanyCreateView.as_view(), name='create-company'),
    path('empresas/<int:pk>/', views.CompanyDetailView.as_view(), name='detail-company'),
    path('empresas/<int:pk>/editar/', views.CompanyUpdateView.as_view(), name='update-company'),
    path('empresas/<int:pk>/excluir/', views.CompanyDeleteView.as_view(), name='delete-company'),
    
    # Contract URLs
    path('contratos/', views.ContractListView.as_view(), name='contract-list'),
    path('contratos/novo/', views.ContractCreateView.as_view(), name='create-contract'),
    path('contratos/<int:pk>/', views.ContractDetailView.as_view(), name='detail-contract'),
    path('contratos/<int:pk>/editar/', views.ContractUpdateView.as_view(), name='update-contract'),
    path('contratos/<int:pk>/excluir/', views.ContractDeleteView.as_view(), name='delete-contract'),
    
    # State URLs (Admin only)
    path('estados/', views.StateListView.as_view(), name='state-list'),
    path('estados/novo/', views.StateCreateView.as_view(), name='create-state'),
    path('estados/<int:pk>/editar/', views.StateUpdateView.as_view(), name='update-state'),
    path('estados/<int:pk>/excluir/', views.StateDeleteView.as_view(), name='delete-state'),
    
    # City URLs (Admin only)
    path('cidades/', views.CityListView.as_view(), name='city-list'),
    path('cidades/nova/', views.CityCreateView.as_view(), name='create-city'),
    path('cidades/<int:pk>/editar/', views.CityUpdateView.as_view(), name='update-city'),
    path('cidades/<int:pk>/excluir/', views.CityDeleteView.as_view(), name='delete-city'),
]
