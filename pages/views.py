# IMPORTS SEGUROS
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, FormView, View, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from datetime import timedelta
from .models import Person, Company, Contract, State, City

# IMPORTAR MIXINS DO PRÓPRIO APP (LOCAL)
from .mixins import (
    OwnerQuerysetMixin, 
    OwnerObjectPermissionMixin, 
    OwnerCreateMixin,
    AdminOnlyMixin,
    GroupRequiredMixin,
    FuncionarioRequiredMixin,
    AdminRequiredMixin,
    StaffRequiredMixin
)

# ✅ IMPORTAR FORMS CUSTOMIZADOS
from .forms import PersonForm, CompanyForm, ContractForm, StateForm, CityForm

# ===========================================
# VIEWS BÁSICAS (INDEX, ABOUT, HOME)
# ===========================================

class IndexView(TemplateView):
    """Página inicial pública"""
    template_name = 'pages/index.html'

class AboutView(TemplateView):
    """Página sobre o sistema"""
    template_name = 'pages/about.html'

# ✅ REDIRECT TEMPORÁRIO PARA about/ → sobre/
class AboutRedirectView(RedirectView):
    """Redirect de /about/ para /sobre/ para compatibilidade"""
    pattern_name = 'about'
    permanent = True

class HomeView(TemplateView):
    """Dashboard principal com KPIs e registros recentes - permite acesso anônimo"""
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # Para usuários autenticados, calcular KPIs
            user = self.request.user
            
            # Se for superuser ou admin, ver tudo
            if user.is_superuser or user.groups.filter(name='empresa_admin').exists():
                pessoas = Person.objects.all()
                empresas = Company.objects.all()
                contratos = Contract.objects.all()
            else:
                # Funcionário comum vê apenas seus dados
                pessoas = Person.objects.filter(usuario=user)
                empresas = Company.objects.filter(usuario=user)
                contratos = Contract.objects.filter(usuario=user)
            
            # KPIs básicos
            context.update({
                'total_pessoas': pessoas.count(),
                'total_empresas': empresas.count(),
                'total_contratos': contratos.count(),
                'total_usuarios': User.objects.count() if user.is_superuser else None,
            })
            
            # Registros recentes (últimos 5)
            context.update({
                'ultimas_pessoas': pessoas.order_by('-created_at')[:5],
                'ultimas_empresas': empresas.order_by('-created_at')[:5], 
                'ultimos_contratos': contratos.order_by('-created_at')[:5],
            })
            
            # Estatísticas temporais
            uma_semana_atras = timezone.now() - timedelta(days=7)
            context['pessoas_ultima_semana'] = pessoas.filter(created_at__gte=uma_semana_atras).count()
        
        return context

# ===========================================
# VIEWS PARA PERSON (PESSOA) - COM PROTEÇÃO
# ===========================================

class PersonListView(FuncionarioRequiredMixin, OwnerQuerysetMixin, ListView):
    """ListView para pessoas - requer grupo funcionario + escopo por usuário"""
    model = Person
    template_name = 'pages/lists/person_list.html'
    context_object_name = 'persons'
    paginate_by = 10

class PersonCreateView(LoginRequiredMixin, OwnerCreateMixin, CreateView):
    """Criação de pessoa"""
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/person_form.html'
    success_url = reverse_lazy('person-list')
    
    def get_form_kwargs(self):
        """Passa o usuário para o formulário"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """✅ GARANTIR QUE O USUARIO_ID SEJA PREENCHIDO"""
        form.instance.usuario = self.request.user
        messages.success(self.request, f'Pessoa "{form.instance.full_name}" cadastrada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao criar pessoa. Verifique os dados.')
        return super().form_invalid(form)

class PersonDetailView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DetailView):
    """DetailView para pessoas - requer grupo funcionario + ownership"""
    model = Person
    template_name = 'pages/detail/person_detail.html'
    context_object_name = 'person'

class PersonUpdateView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, UpdateView):
    """UpdateView para pessoas - requer grupo funcionario + ownership"""
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/person_form.html'
    success_url = reverse_lazy('person-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Pessoa "{form.instance.full_name}" atualizada com sucesso!')
        return super().form_valid(form)

class PersonDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DeleteView):
    """DeleteView para pessoas - requer grupo funcionario + ownership"""
    model = Person
    template_name = 'pages/confirm/person_confirm_delete.html'
    success_url = reverse_lazy('person-list')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'✅ Pessoa "{obj.full_name}" excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA COMPANY (EMPRESA) - COM PROTEÇÃO
# ===========================================

class CompanyListView(FuncionarioRequiredMixin, OwnerQuerysetMixin, ListView):
    """ListView para empresas - requer grupo funcionario + escopo por usuário"""
    model = Company
    template_name = 'pages/lists/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10

class CompanyCreateView(OwnerCreateMixin, FuncionarioRequiredMixin, CreateView):
    """CreateView para empresas - requer grupo funcionario"""
    model = Company
    form_class = CompanyForm
    template_name = 'pages/forms/company_form.html'
    success_url = reverse_lazy('company-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """✅ GARANTIR QUE O USUARIO_ID SEJA PREENCHIDO"""
        form.instance.usuario = self.request.user
        messages.success(self.request, f'✅ Empresa "{form.instance.corporate_name}" criada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao criar empresa. Verifique os dados.')
        return super().form_invalid(form)

class CompanyDetailView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DetailView):
    """DetailView para empresas - requer grupo funcionario + ownership"""
    model = Company
    template_name = 'pages/detail/company_detail.html'
    context_object_name = 'company'

class CompanyUpdateView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, UpdateView):
    """UpdateView para empresas - requer grupo funcionario + ownership"""
    model = Company
    form_class = CompanyForm
    template_name = 'pages/forms/company_form.html'
    success_url = reverse_lazy('company-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Empresa "{form.instance.corporate_name}" atualizada com sucesso!')
        return super().form_valid(form)

class CompanyDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DeleteView):
    """DeleteView para empresas - requer grupo funcionario + ownership"""
    model = Company
    template_name = 'pages/confirm/company_confirm_delete.html'
    success_url = reverse_lazy('company-list')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'✅ Empresa "{obj.corporate_name}" excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA CONTRACT (CONTRATO) - COM PROTEÇÃO
# ===========================================

class ContractListView(FuncionarioRequiredMixin, OwnerQuerysetMixin, ListView):
    """ListView para contratos - requer grupo funcionario + escopo por usuário"""
    model = Contract
    template_name = 'pages/lists/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 10

class ContractCreateView(LoginRequiredMixin, OwnerCreateMixin, CreateView):
    """CreateView para contratos"""
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    success_url = reverse_lazy('contract-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """✅ GARANTIR QUE O USUARIO_ID SEJA PREENCHIDO"""
        form.instance.usuario = self.request.user
        messages.success(self.request, f'✅ Contrato "{form.instance.title}" criado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao criar contrato. Verifique os dados.')
        return super().form_invalid(form)

class ContractDetailView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DetailView):
    """DetailView para contratos - requer grupo funcionario + ownership"""
    model = Contract
    template_name = 'pages/detail/contract_detail.html'
    context_object_name = 'contract'

class ContractUpdateView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, UpdateView):
    """UpdateView para contratos - requer grupo funcionario + ownership"""
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    success_url = reverse_lazy('contract-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Contrato "{form.instance.title}" atualizado com sucesso!')
        return super().form_valid(form)

class ContractDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DeleteView):
    """DeleteView para contratos - requer grupo funcionario + ownership"""
    model = Contract
    template_name = 'pages/confirm/contract_confirm_delete.html'
    success_url = reverse_lazy('contract-list')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'✅ Contrato "{obj.title}" excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA STATE (ESTADO) - APENAS ADMIN
# ===========================================

class StateListView(AdminRequiredMixin, ListView):
    """ListView para estados - APENAS empresa_admin"""
    model = State
    template_name = 'pages/lists/state_list.html'
    context_object_name = 'states'
    paginate_by = 20

class StateCreateView(AdminRequiredMixin, CreateView):
    """CreateView para estados - APENAS empresa_admin"""
    model = State
    form_class = StateForm
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class StateUpdateView(AdminRequiredMixin, UpdateView):
    """UpdateView para estados - APENAS empresa_admin"""
    model = State
    form_class = StateForm
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class StateDeleteView(AdminRequiredMixin, DeleteView):
    """DeleteView para estados - APENAS empresa_admin"""
    model = State
    template_name = 'pages/confirm/state_confirm_delete.html'
    success_url = reverse_lazy('state-list')

# ===========================================
# VIEWS PARA CITY (CIDADE) - APENAS ADMIN
# ===========================================

class CityListView(AdminRequiredMixin, ListView):
    """ListView para cidades - APENAS empresa_admin"""
    model = City
    template_name = 'pages/lists/city_list.html'
    context_object_name = 'cities'
    paginate_by = 20

class CityCreateView(AdminRequiredMixin, CreateView):
    """CreateView para cidades - APENAS empresa_admin"""
    model = City
    form_class = CityForm
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class CityDetailView(AdminRequiredMixin, DetailView):
    """DetailView para cidades - APENAS empresa_admin"""
    model = City
    template_name = 'pages/detail/city_detail.html'
    context_object_name = 'city'

class CityUpdateView(AdminRequiredMixin, UpdateView):
    """UpdateView para cidades - APENAS empresa_admin"""
    model = City
    form_class = CityForm
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class CityDeleteView(AdminRequiredMixin, DeleteView):
    """DeleteView para cidades - APENAS empresa_admin"""
    model = City
    template_name = 'pages/confirm/city_confirm_delete.html'
    success_url = reverse_lazy('city-list')

# ===========================================
# VIEWS PARA RASCUNHOS DE CONTRATOS (PÚBLICO)
# ===========================================

class ContractDraftStartView(LoginRequiredMixin, FormView):
    """Início do rascunho de contrato"""
    template_name = 'pages/contracts/contract_draft_form.html'
    form_class = ContractForm
    
    def get_success_url(self):
        return reverse_lazy('contract-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        """✅ GARANTIR QUE O USUARIO_ID SEJA PREENCHIDO"""
        contract = form.save(commit=False)
        contract.usuario = self.request.user
        contract.save()
        messages.success(self.request, f'✅ Contrato "{contract.title}" criado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao criar contrato. Verifique os dados.')
        return super().form_invalid(form)

class ContratoDraftReviewView(TemplateView):
    """Revisão de rascunho - permite anônimo"""
    template_name = 'pages/contratos/contrato_draft_review.html'

class ContratoDraftFinalizeView(FuncionarioRequiredMixin, TemplateView):
    """Finalização de rascunho - requer autenticação"""
    template_name = 'pages/contratos/contrato_draft_finalize.html'