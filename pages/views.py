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

from .models import Person, Company, Contract, State, City, ContractMovement  # ✅ ADICIONAR ContractMovement
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
from .filters import PersonFilter, CompanyFilter, ContractFilter, StateFilter, CityFilter  # ✅ NOVO IMPORT

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
# CONTRACT VIEWS
# ===========================================

class ContractListView(OwnerQuerysetMixin, FuncionarioRequiredMixin, FilterView):
    """ListView com filtros para contratos"""
    model = Contract
    template_name = 'pages/lists/contract_list.html'
    context_object_name = 'contracts'
    filterset_class = ContractFilter
    paginate_by = 10
    
    def get_queryset(self):
        return super().get_queryset().select_related('company', 'person', 'usuario').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_contracts'] = self.get_queryset().count()
        return context


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
        contract = form.save(commit=False)
        contract.usuario = self.request.user
        contract.save()
        form.save_m2m()
        
        # ✅ REGISTRAR MOVIMENTO
        ContractMovement.objects.create(
            contract=contract,
            movement_type='created',
            description=f'Contrato criado por {self.request.user.username}',
            performed_by=self.request.user,
            metadata={
                'title': contract.title,
                'company_id': contract.company.id if contract.company else None,
                'person_id': contract.person.id if contract.person else None,
            }
        )
        
        # ✅ ATUALIZAR CONTADOR NA EMPRESA
        if contract.company:
            contract.company.total_contracts = contract.company.contracts.filter(is_active=True).count()
            contract.company.save(update_fields=['total_contracts'])
        
        messages.success(
            self.request, 
            f'✅ Contrato "{contract.title}" criado com sucesso!'
        )
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        messages.error(
            self.request, 
            '❌ Erro ao criar contrato. Verifique os dados informados.'
        )
        return super().form_invalid(form)


class ContractDetailView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DetailView):
    """DetailView para contratos"""
    model = Contract
    template_name = 'pages/detail/contract_detail.html'
    context_object_name = 'contract'
    
    def get_queryset(self):
        return super().get_queryset().select_related('company', 'person', 'usuario')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ✅ ADICIONAR MOVIMENTOS AO CONTEXTO
        context['movements'] = self.object.movements.select_related('performed_by').order_by('-created_at')[:10]
        return context


class ContractUpdateView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, UpdateView):
    """UpdateView para contratos"""
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    success_url = reverse_lazy('contract-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        contract = form.save(commit=False)
        
        # ✅ DETECTAR MUDANÇAS
        changed_fields = []
        if form.changed_data:
            changed_fields = list(form.changed_data)
        
        contract.save()
        form.save_m2m()
        
        # ✅ REGISTRAR MOVIMENTO
        ContractMovement.objects.create(
            contract=contract,
            movement_type='updated',
            description=f'Contrato atualizado por {self.request.user.username}',
            performed_by=self.request.user,
            metadata={
                'changed_fields': changed_fields,
                'title': contract.title,
            }
        )
        
        # ✅ ATUALIZAR CONTADOR NA EMPRESA
        if contract.company:
            contract.company.total_contracts = contract.company.contracts.filter(is_active=True).count()
            contract.company.save(update_fields=['total_contracts'])
        
        messages.success(
            self.request, 
            f'✅ Contrato "{contract.title}" atualizado com sucesso!'
        )
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        messages.error(
            self.request, 
            '❌ Erro ao atualizar contrato. Verifique os dados informados.'
        )
        return super().form_invalid(form)


class ContractDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DeleteView):
    """DeleteView para contratos"""
    model = Contract
    template_name = 'pages/confirm/contract_confirm_delete.html'
    success_url = reverse_lazy('contract-list')
    
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        contract_title = obj.title
        company = obj.company
        
        # ✅ REGISTRAR MOVIMENTO ANTES DE DELETAR
        ContractMovement.objects.create(
            contract=obj,
            movement_type='deleted',
            description=f'Contrato excluído por {request.user.username}',
            performed_by=request.user,
            metadata={
                'title': contract_title,
                'company_id': company.id if company else None,
                'deleted_at': timezone.now().isoformat(),
            }
        )
        
        # ✅ MENSAGEM DE SUCESSO
        messages.success(
            request, 
            f'✅ Contrato "{contract_title}" excluído com sucesso!'
        )
        
        # ✅ DELETAR OBJETO
        response = super().delete(request, *args, **kwargs)
        
        # ✅ ATUALIZAR CONTADOR NA EMPRESA (DEPOIS DA EXCLUSÃO)
        if company:
            company.total_contracts = company.contracts.filter(is_active=True).count()
            company.save(update_fields=['total_contracts'])
        
        return response


# =====================================================
# STATE VIEWS
# =====================================================

class StateListView(AdminRequiredMixin, FilterView):
    """Lista de estados - APENAS ADMIN"""
    model = State
    template_name = 'pages/lists/state_list.html'
    context_object_name = 'states'
    filterset_class = StateFilter
    paginate_by = 25


class StateCreateView(AdminRequiredMixin, CreateView):
    """Criar estado - APENAS ADMIN"""
    model = State
    form_class = StateForm
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Estado criado com sucesso!')
        return super().form_valid(form)


class StateDetailView(AdminRequiredMixin, DetailView):
    """Detalhes do estado - APENAS ADMIN"""
    model = State
    template_name = 'pages/details/state_detail.html'
    context_object_name = 'state'


class StateUpdateView(AdminRequiredMixin, UpdateView):
    """Editar estado - APENAS ADMIN"""
    model = State
    form_class = StateForm
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Estado atualizado com sucesso!')
        return super().form_valid(form)


class StateDeleteView(AdminRequiredMixin, DeleteView):
    """Deletar estado - APENAS ADMIN"""
    model = State
    template_name = 'pages/confirms/state_confirm_delete.html'
    success_url = reverse_lazy('state-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '✅ Estado excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


# ====================================
# CITY VIEWS
# ====================================

class CityListView(LoginRequiredMixin, ListView):
    model = City
    template_name = 'pages/lists/city_list.html'
    context_object_name = 'cities'
    paginate_by = 10

    def get_queryset(self):
        queryset = City.objects.select_related('state').order_by('name')
        
        # Apply filters
        self.filterset = CityFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['total_cities'] = self.filterset.qs.count()
        return context


class CityDetailView(LoginRequiredMixin, DetailView):
    model = City
    template_name = 'pages/detail/city_detail.html'
    context_object_name = 'city'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.get_object()
        
        # Breadcrumbs
        context['breadcrumbs'] = [
            {'title': 'Home', 'url': 'home'},
            {'title': 'Cidades', 'url': 'city-list'},
            {'title': city.name, 'url': None}
        ]
        
        return context


class CityCreateView(AdminRequiredMixin, CreateView):
    """CreateView para cidades - APENAS empresa_admin"""
    model = City
    form_class = CityForm
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Cidade "{form.instance.name}" criada com sucesso!')
        return super().form_valid(form)


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
# Deploy 2025-11-04 23:39:16
