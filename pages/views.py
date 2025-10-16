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
from django_filters.views import FilterView  # ✅ NOVO IMPORT

from .models import Person, Company, Contract, State, City
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
from .forms import PersonForm, CompanyForm, ContractForm, StateForm, CityForm
from .filters import ContractFilter, CompanyFilter, PersonFilter  # ✅ NOVO IMPORT

# ===========================================
# VIEWS BÁSICAS (INDEX, ABOUT, HOME)
# ===========================================

class IndexView(TemplateView):
    """View para index (página inicial pública)"""
    template_name = 'pages/index.html'


class AboutView(TemplateView):
    """View para About (sobre o sistema)"""
    template_name = 'pages/about.html'


class AboutRedirectView(RedirectView):
    """Redireciona /about/ para /sobre/"""
    pattern_name = 'about'
    permanent = True


class HomeView(LoginRequiredMixin, TemplateView):
    """View para Home (dashboard após login)"""
    template_name = 'pages/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # ✅ OTIMIZADO: Contar sem N+1
        context['total_persons'] = Person.objects.filter(usuario=user).count()
        context['total_companies'] = Company.objects.filter(usuario=user).count()
        context['total_contracts'] = Contract.objects.filter(usuario=user).count()
        
        # ✅ OTIMIZADO: Buscar registros recentes com select_related
        context['recent_persons'] = Person.objects.filter(
            usuario=user
        ).select_related('city__state').order_by('-created_at')[:5]
        
        context['recent_companies'] = Company.objects.filter(
            usuario=user
        ).select_related('city__state').order_by('-created_at')[:5]
        
        context['recent_contracts'] = Contract.objects.filter(
            usuario=user
        ).select_related('company', 'person', 'usuario').order_by('-created_at')[:5]
        
        return context


# ===========================================
# VIEWS PARA PERSON (PESSOA) - COM PROTEÇÃO
# ===========================================

class PersonListView(FuncionarioRequiredMixin, OwnerQuerysetMixin, FilterView):
    """ListView para pessoas - requer grupo funcionario + escopo por usuário"""
    model = Person
    template_name = 'pages/lists/person_list.html'
    context_object_name = 'persons'
    paginate_by = 10
    filterset_class = PersonFilter  # ✅ NOVO
    
    # ✅ OTIMIZAÇÃO N+1: select_related para FK city e city.state
    def get_queryset(self):
        qs = super().get_queryset()
        # FK: usuario (owner), city, city.state
        qs = qs.select_related('usuario', 'city', 'city__state')
        return qs


class PersonCreateView(LoginRequiredMixin, OwnerCreateMixin, CreateView):
    """CreateView para pessoas"""
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/person_form.html'
    success_url = reverse_lazy('person-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, f'✅ Pessoa "{form.instance.full_name}" criada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao criar pessoa. Verifique os dados.')
        return super().form_invalid(form)


class PersonDetailView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DetailView):
    """DetailView para pessoas - requer grupo funcionario + ownership"""
    model = Person
    template_name = 'pages/detail/person_detail.html'
    context_object_name = 'person'
    
    # ✅ OTIMIZAÇÃO N+1: select_related + prefetch_related
    def get_queryset(self):
        qs = super().get_queryset()
        # FK: usuario, city, city.state
        qs = qs.select_related('usuario', 'city', 'city__state')
        # Reverse FK: contracts (pessoa -> contratos)
        qs = qs.prefetch_related('contracts', 'contracts__company')
        return qs


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

class CompanyListView(FuncionarioRequiredMixin, OwnerQuerysetMixin, FilterView):
    """ListView para empresas - requer grupo funcionario + escopo por usuário"""
    model = Company
    template_name = 'pages/lists/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10
    filterset_class = CompanyFilter  # ✅ NOVO
    
    # ✅ OTIMIZAÇÃO N+1: select_related para FK
    def get_queryset(self):
        qs = super().get_queryset()
        # FK: usuario (owner), city, city.state
        qs = qs.select_related('usuario', 'city', 'city__state')
        return qs


class CompanyCreateView(LoginRequiredMixin, OwnerCreateMixin, CreateView):
    """CreateView para empresas"""
    model = Company
    form_class = CompanyForm
    template_name = 'pages/forms/company_form.html'
    success_url = reverse_lazy('company-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
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
    
    # ✅ OTIMIZAÇÃO N+1: select_related + prefetch_related
    def get_queryset(self):
        qs = super().get_queryset()
        # FK: usuario, city, city.state
        qs = qs.select_related('usuario', 'city', 'city__state')
        # Reverse FK: contracts (empresa -> contratos)
        qs = qs.prefetch_related('contracts', 'contracts__person')
        return qs


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

class ContractListView(FuncionarioRequiredMixin, OwnerQuerysetMixin, FilterView):
    """ListView para contratos - requer grupo funcionario + escopo por usuário"""
    model = Contract
    template_name = 'pages/lists/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 10
    filterset_class = ContractFilter  # ✅ NOVO
    
    # ✅ OTIMIZAÇÃO N+1: select_related para todas as FKs
    def get_queryset(self):
        qs = super().get_queryset()
        # FK: usuario (owner), company, person
        qs = qs.select_related('usuario', 'company', 'person')
        # Nested FK: company.city, person.city
        qs = qs.select_related('company__city', 'person__city')
        return qs


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
    
    # ✅ OTIMIZAÇÃO N+1: select_related para todas as relações
    def get_queryset(self):
        qs = super().get_queryset()
        # FK: usuario, company, person
        qs = qs.select_related('usuario', 'company', 'person')
        # Nested FK: company.city, person.city, city.state
        qs = qs.select_related(
            'company__city', 'company__city__state',
            'person__city', 'person__city__state'
        )
        return qs


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
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Estado "{form.instance.name}" criado com sucesso!')
        return super().form_valid(form)


class StateUpdateView(AdminRequiredMixin, UpdateView):
    """UpdateView para estados - APENAS empresa_admin"""
    model = State
    form_class = StateForm
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Estado "{form.instance.name}" atualizado com sucesso!')
        return super().form_valid(form)


class StateDeleteView(AdminRequiredMixin, DeleteView):
    """DeleteView para estados - APENAS empresa_admin"""
    model = State
    template_name = 'pages/confirm/state_confirm_delete.html'
    success_url = reverse_lazy('state-list')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'✅ Estado "{obj.name}" excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# ===========================================
# VIEWS PARA CITY (CIDADE) - APENAS ADMIN
# ===========================================

class CityListView(AdminRequiredMixin, ListView):
    """ListView para cidades - APENAS empresa_admin"""
    model = City
    template_name = 'pages/lists/city_list.html'
    context_object_name = 'cities'
    paginate_by = 20
    
    # ✅ OTIMIZAÇÃO N+1: select_related para FK state
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('state')
        return qs


class CityCreateView(AdminRequiredMixin, CreateView):
    """CreateView para cidades - APENAS empresa_admin"""
    model = City
    form_class = CityForm
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Cidade "{form.instance.name}" criada com sucesso!')
        return super().form_valid(form)


class CityDetailView(AdminRequiredMixin, DetailView):
    """DetailView para cidades - APENAS empresa_admin"""
    model = City
    template_name = 'pages/detail/city_detail.html'
    context_object_name = 'city'
    
    # ✅ OTIMIZAÇÃO N+1
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('state')
        return qs


class CityUpdateView(AdminRequiredMixin, UpdateView):
    """UpdateView para cidades - APENAS empresa_admin"""
    model = City
    form_class = CityForm
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Cidade "{form.instance.name}" atualizada com sucesso!')
        return super().form_valid(form)


class CityDeleteView(AdminRequiredMixin, DeleteView):
    """DeleteView para cidades - APENAS empresa_admin"""
    model = City
    template_name = 'pages/confirm/city_confirm_delete.html'
    success_url = reverse_lazy('city-list')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'✅ Cidade "{obj.name}" excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


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
    template_name = 'pages/contracts/contract_draft_review.html'


class ContratoDraftFinalizeView(FuncionarioRequiredMixin, TemplateView):
    """Finalização de rascunho - requer autenticação"""
    template_name = 'pages/contracts/contract_draft_finalize.html'