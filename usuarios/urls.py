from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # URLs de autenticação básicas
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    # LOGOUT SIMPLES - só aceita POST
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # ALTERAR SENHA - se quiser adicionar no futuro
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(
        template_name='usuarios/change_password.html',
        success_url='/usuarios/alterar-senha/concluido/'
    ), name='alterar-senha'),
    path('alterar-senha/concluido/', auth_views.PasswordChangeDoneView.as_view(
        template_name='usuarios/change_password_done.html'
    ), name='password_change_done'),
    
    # Cadastro de usuários
    path('cadastro/', views.EscolhaTipoCadastroView.as_view(), name='escolha-tipo-cadastro'),
    path('cadastro/pessoa-fisica/', views.CadastroPessoaFisicaView.as_view(), name='cadastro-pf'),
    path('cadastro/pessoa-juridica/', views.CadastroPessoaJuridicaView.as_view(), name='cadastro-pj'),
    
    # Perfil
    path('perfil/', views.perfil_view, name='perfil'),
]