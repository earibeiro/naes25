from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views  # ✅ USAR IMPORT SIMPLES
from .views import (
    EscolhaTipoCadastroView,
    SignUpEmpresaAdminView,
    SignUpFuncionarioView,
    CadastroPessoaFisicaView,
    CadastroPessoaJuridicaView,
    CustomLogoutView,
    CustomLoginView,  # ✅ ADICIONAR
    AdminSignupView,   # ✅ ADICIONAR
    FuncionarioSignupView,  # ✅ ADICIONAR
    PerfilView,        # ✅ ADICIONAR
    teste_view
)

# ✅ CORRIGIR IMPORT DO FORM
try:
    from .forms import CustomPasswordChangeForm
except ImportError:
    CustomPasswordChangeForm = None

app_name = "usuarios"

urlpatterns = [
    # Login/Logout
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # Cadastro
    path('cadastro/', EscolhaTipoCadastroView.as_view(), name='cadastro-escolha'),
    path('cadastro/admin/', AdminSignupView.as_view(), name='cadastro-admin'),
    path('cadastro/funcionario/', FuncionarioSignupView.as_view(), name='cadastro-funcionario'),
    path('cadastro/pessoa-fisica/', CadastroPessoaFisicaView.as_view(), name='cadastro-pessoa-fisica'),
    path('cadastro/pessoa-juridica/', CadastroPessoaJuridicaView.as_view(), name='cadastro-pessoa-juridica'),
    
    # Perfil
    path('perfil/', PerfilView.as_view(), name='perfil'),
    
    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='usuarios/password_reset.html'
    ), name='password_reset'),
    
    # Rotas antigas (compatibilidade)
    path('cadastro-pj/', CadastroPessoaJuridicaView.as_view(), name='cadastro-pj'),
    path('cadastro-pf/', CadastroPessoaFisicaView.as_view(), name='cadastro-pf'),
    
    # Alteração de senha
    path('alterar-senha/', auth_views.PasswordChangeView.as_view(
        template_name='usuarios/change_password.html',
        form_class=CustomPasswordChangeForm if CustomPasswordChangeForm else None,
        success_url=reverse_lazy('home')
    ), name='change-password'),
    
    path('senha-alterada/', auth_views.PasswordChangeDoneView.as_view(
        template_name='usuarios/password_change_done.html'
    ), name='password-change-done'),
    
    # Teste
    path('teste/', teste_view, name='teste'),
]

# Deploy: 2025-11-06 14:00:00
