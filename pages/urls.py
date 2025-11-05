from django.urls import path
from . import views

urlpatterns = [
    # ✅ HOME (SEMPRE USAR .as_view() PARA CLASS-BASED VIEWS)
    path('', views.HomeView.as_view(), name='home'),
    
    # Person URLs
    path('pessoas/', views.PersonListView.as_view(), name='person-list'),
    path('pessoas/criar/', views.PersonCreateView.as_view(), name='person-create'),
    path('pessoas/<int:pk>/', views.PersonDetailView.as_view(), name='person-detail'),
    path('pessoas/<int:pk>/editar/', views.PersonUpdateView.as_view(), name='person-update'),
    path('pessoas/<int:pk>/deletar/', views.PersonDeleteView.as_view(), name='person-delete'),
    
    # Company URLs
    path('empresas/', views.CompanyListView.as_view(), name='company-list'),
    path('empresas/criar/', views.CompanyCreateView.as_view(), name='company-create'),
    path('empresas/<int:pk>/', views.CompanyDetailView.as_view(), name='company-detail'),
    path('empresas/<int:pk>/editar/', views.CompanyUpdateView.as_view(), name='company-update'),
    path('empresas/<int:pk>/deletar/', views.CompanyDeleteView.as_view(), name='company-delete'),
    
    # Contract URLs
    path('contratos/', views.ContractListView.as_view(), name='contract-list'),
    path('contratos/criar/', views.ContractCreateView.as_view(), name='contract-create'),
    path('contratos/<int:pk>/', views.ContractDetailView.as_view(), name='contract-detail'),
    path('contratos/<int:pk>/editar/', views.ContractUpdateView.as_view(), name='contract-update'),
    path('contratos/<int:pk>/deletar/', views.ContractDeleteView.as_view(), name='contract-delete'),
    
    # ✅ STATE URLs (VERIFICAR SE StateDetailView EXISTE)
    path('estados/', views.StateListView.as_view(), name='state-list'),
    path('estados/criar/', views.StateCreateView.as_view(), name='state-create'),
    path('estados/<int:pk>/', views.StateDetailView.as_view(), name='state-detail'),  # ✅ VERIFICAR
    path('estados/<int:pk>/editar/', views.StateUpdateView.as_view(), name='state-update'),
    path('estados/<int:pk>/deletar/', views.StateDeleteView.as_view(), name='state-delete'),
    
    # City URLs
    path('cidades/', views.CityListView.as_view(), name='city-list'),
    path('cidades/criar/', views.CityCreateView.as_view(), name='city-create'),
    path('cidades/<int:pk>/', views.CityDetailView.as_view(), name='city-detail'),
    path('cidades/<int:pk>/editar/', views.CityUpdateView.as_view(), name='city-update'),
    path('cidades/<int:pk>/deletar/', views.CityDeleteView.as_view(), name='city-delete'),
    
    # Contract Draft URLs (anonymous access)
    path('rascunho/contrato/', views.ContractDraftStartView.as_view(), name='contrato-draft-start'),
    path('rascunho/revisar/', views.ContratoDraftReviewView.as_view(), name='contrato-draft-review'),
    path('rascunho/finalizar/', views.ContratoDraftFinalizeView.as_view(), name='contrato-draft-finalize'),
    
    # About URLs
    path('sobre/', views.AboutView.as_view(), name='about'),
    path('about/', views.AboutRedirectView.as_view()),  # Redirect /about/ → /sobre/
    
    # Index
    path('index/', views.IndexView.as_view(), name='index'),
]

# Deploy 2025-11-04 23:39:16
