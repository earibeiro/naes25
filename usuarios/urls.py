from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    EscolhaTipoCadastroView,
    SignUpEmpresaAdminView,
    SignUpFuncionarioView,
    CadastroPessoaFisicaView,
    CadastroPessoaJuridicaView,
    CustomLogoutView,
    teste_view
)

# ✅ CORRIGIR IMPORT DO FORM
try:
    from .forms import CustomPasswordChangeForm
except ImportError:
    # Fallback se form não existir
    CustomPasswordChangeForm = None

app_name = "usuarios"

urlpatterns = [
    # Novas rotas de cadastro
    path("cadastro/", EscolhaTipoCadastroView.as_view(), name="cadastro-escolha"),
    path("cadastro/admin/", SignUpEmpresaAdminView.as_view(), name="cadastro-admin"),
    path("cadastro/funcionario/", SignUpFuncionarioView.as_view(), name="cadastro-funcionario"),
    
    # Rotas existentes para compatibilidade
    path('escolha-tipo-cadastro/', EscolhaTipoCadastroView.as_view(), name='escolha-tipo-cadastro'),
    path('cadastro-pessoa-fisica/', CadastroPessoaFisicaView.as_view(), name='cadastro-pessoa-fisica'),
    path('cadastro-pessoa-juridica/', CadastroPessoaJuridicaView.as_view(), name='cadastro-pessoa-juridica'),
    
    # Adicionar rota que pode estar sendo referenciada em templates antigos
    path('cadastro-pj/', CadastroPessoaJuridicaView.as_view(), name='cadastro-pj'),
    path('cadastro-pf/', CadastroPessoaFisicaView.as_view(), name='cadastro-pf'),
    
    # Login/Logout específicos
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    # ✅ ALTERAÇÃO DE SENHA COM FORM OPCIONAL
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