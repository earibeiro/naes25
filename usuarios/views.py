from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model

from .forms import (
    CadastroPessoaFisicaForm, 
    CadastroPessoaJuridicaForm,
    AdminSignupForm,
    FuncionarioSignupForm
)
from .models import UserProfile

User = get_user_model()


class EscolhaTipoCadastroView(TemplateView):
    """View para escolher tipo de cadastro"""
    template_name = "usuarios/escolha_tipo_cadastro.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["next"] = self.request.GET.get("next", "")
        return ctx


class SignUpEmpresaAdminView(CreateView):
    """Cadastro de Empresa/Administrador"""
    template_name = "usuarios/signup_admin.html"
    form_class = AdminSignupForm
    success_url = reverse_lazy("home")

    def get_success_url(self):
        # Respeita ?next=
        nxt = self.request.GET.get("next")
        return nxt or super().get_success_url()

    def form_valid(self, form):
        resp = super().form_valid(form)
        login(self.request, self.object)
        messages.success(
            self.request, 
            f'✅ Conta de administrador criada com sucesso! Bem-vindo, {self.object.username}!'
        )
        return resp

    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao criar conta. Verifique os dados informados.')
        return super().form_invalid(form)


class SignUpFuncionarioView(CreateView):
    """Cadastro de Funcionário/Colaborador"""
    template_name = "usuarios/signup_funcionario.html"
    form_class = FuncionarioSignupForm
    success_url = reverse_lazy("home")

    def get_success_url(self):
        nxt = self.request.GET.get("next")
        return nxt or super().get_success_url()

    def form_valid(self, form):
        resp = super().form_valid(form)
        login(self.request, self.object)
        messages.success(
            self.request, 
            f'✅ Conta de funcionário criada com sucesso! Bem-vindo, {self.object.username}!'
        )
        return resp

    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao criar conta. Verifique os dados informados.')
        return super().form_invalid(form)


# MANTER VIEWS EXISTENTES PARA COMPATIBILIDADE
class CadastroPessoaFisicaView(SignUpFuncionarioView):
    """View para cadastro de Pessoa Física (alias)"""
    template_name = "usuarios/cadastro_pessoa_fisica.html"
    form_class = CadastroPessoaFisicaForm


class CadastroPessoaJuridicaView(SignUpEmpresaAdminView):
    """View para cadastro de Pessoa Jurídica (alias)"""
    template_name = "usuarios/cadastro_pessoa_juridica.html"
    form_class = CadastroPessoaJuridicaForm


# LOGOUT SEGURO - só aceita POST
class CustomLogoutView(LogoutView):
    """Logout customizado que só aceita POST"""
    http_method_names = ['post']  # ✅ FORÇAR APENAS POST
    
    def post(self, request, *args, **kwargs):
        """Processa logout via POST com mensagem"""
        user = request.user
        if user.is_authenticated:
            messages.success(request, f'Logout realizado com sucesso para {user.username}!')
        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """Bloquear GET e mostrar aviso"""
        messages.warning(request, '⚠️ Logout deve ser feito via POST por segurança.')
        return redirect('home')


# View simples para teste (pode remover depois)
def teste_view(request):
    return render(request, 'usuarios/teste.html', {
        'titulo': 'Teste de Usuários',
        'user': request.user
    })

# Deploy: 2025-11-06 00:04:16
