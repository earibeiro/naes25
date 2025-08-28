from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import CadastroPessoaFisicaForm, CadastroPessoaJuridicaForm
from .models import UserProfile

# View simples para teste (pode remover depois)
def teste_view(request):
    return render(request, 'usuarios/teste.html')

class EscolhaTipoCadastroView(TemplateView):
    """View para escolher tipo de cadastro"""
    template_name = 'usuarios/escolha_tipo_cadastro.html'

class CadastroPessoaFisicaView(CreateView):
    """View para cadastro de Pessoa Física"""
    form_class = CadastroPessoaFisicaForm
    template_name = 'usuarios/cadastro_pessoa_fisica.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            f'✅ Conta de Pessoa Física criada com sucesso! '
            f'CPF: {form.cleaned_data["cpf"]}. Faça login para continuar.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request, 
            '❌ Erro ao criar conta de Pessoa Física. Verifique os dados.'
        )
        return super().form_invalid(form)

class CadastroPessoaJuridicaView(CreateView):
    """View para cadastro de Pessoa Jurídica"""
    form_class = CadastroPessoaJuridicaForm
    template_name = 'usuarios/cadastro_pessoa_juridica.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            f'✅ Conta de Pessoa Jurídica criada com sucesso! '
            f'CNPJ: {form.cleaned_data["cnpj"]}. Faça login para continuar.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request, 
            '❌ Erro ao criar conta de Pessoa Jurídica. Verifique os dados.'
        )
        return super().form_invalid(form)

@login_required
def perfil_view(request):
    """View para visualizar perfil do usuário"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.warning(request, 'Perfil não encontrado. Entre em contato com o suporte.')
        profile = None
    
    return render(request, 'usuarios/perfil.html', {
        'profile': profile
    })
