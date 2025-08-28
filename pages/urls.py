from django.urls import path
from . import views

urlpatterns = [
    # Index e páginas estáticas
    path('', views.IndexView.as_view(), name='index'),
    path('home/', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Person URLs - CRUD COMPLETO
    path('pessoas/', views.PersonListView.as_view(), name='person-list'),
    path('pessoas/nova/', views.PersonCreateView.as_view(), name='person-create'),
    path('pessoas/<int:pk>/', views.PersonDetailView.as_view(), name='person-detail'),
    path('pessoas/<int:pk>/editar/', views.PersonUpdateView.as_view(), name='person-update'),
    path('pessoas/<int:pk>/excluir/', views.PersonDeleteView.as_view(), name='person-delete'),
    
    # Company URLs - CRUD COMPLETO
    path('empresas/', views.CompanyListView.as_view(), name='company-list'),
    path('empresas/nova/', views.CompanyCreateView.as_view(), name='company-create'),
    path('empresas/<int:pk>/', views.CompanyDetailView.as_view(), name='company-detail'),
    path('empresas/<int:pk>/editar/', views.CompanyUpdateView.as_view(), name='company-update'),
    path('empresas/<int:pk>/excluir/', views.CompanyDeleteView.as_view(), name='company-delete'),
    
    # Contract URLs - CRUD COMPLETO
    path('contratos/', views.ContractListView.as_view(), name='contract-list'),
    path('contratos/novo/', views.ContractCreateView.as_view(), name='contract-create'),
    path('contratos/<int:pk>/', views.ContractDetailView.as_view(), name='contract-detail'),
    path('contratos/<int:pk>/editar/', views.ContractUpdateView.as_view(), name='contract-update'),
    path('contratos/<int:pk>/excluir/', views.ContractDeleteView.as_view(), name='contract-delete'),
    
    # FLUXO DE RASCUNHO ANÔNIMO
    path('contratos/draft/', views.ContratoDraftStartView.as_view(), name='contrato-draft-start'),
    path('contratos/draft/review/', views.ContratoDraftReviewView.as_view(), name='contrato-draft-review'),
    path('contratos/draft/finalize/', views.ContratoDraftFinalizeView.as_view(), name='contrato-draft-finalize'),

    # State URLs - APENAS ADMIN
    path('admin/estados/', views.StateListView.as_view(), name='state-list'),
    path('admin/estados/novo/', views.StateCreateView.as_view(), name='state-create'),
    path('admin/estados/<int:pk>/editar/', views.StateUpdateView.as_view(), name='state-update'),
    path('admin/estados/<int:pk>/excluir/', views.StateDeleteView.as_view(), name='state-delete'),
    
    # City URLs - APENAS ADMIN
    path('admin/cidades/', views.CityListView.as_view(), name='city-list'),
    path('admin/cidades/nova/', views.CityCreateView.as_view(), name='city-create'),
    path('admin/cidades/<int:pk>/editar/', views.CityUpdateView.as_view(), name='city-update'),
    path('admin/cidades/<int:pk>/excluir/', views.CityDeleteView.as_view(), name='city-delete'),
]
