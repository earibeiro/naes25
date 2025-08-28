from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
)
from braces.views import GroupRequiredMixin
from .models import Person, Company, State, City, Contract
from .forms import PersonForm, CompanyForm, ContractForm, StateForm, CityForm
from django.utils import timezone
from datetime import timedelta

# ===========================================
# VIEWS PARA PERSON (PESSOA FÍSICA)
# ===========================================

class PersonListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Person
    template_name = 'pages/lists/person_list.html'
    context_object_name = 'persons'
    paginate_by = 10
    
    def get_queryset(self):
        return Person.objects.filter(usuario=self.request.user)

class PersonDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Person
    template_name = 'pages/detail/person_detail.html'
    context_object_name = 'person'
    
    def get_queryset(self):
        return Person.objects.filter(usuario=self.request.user)

class PersonCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/person_form.html'
    success_url = reverse_lazy('person-list')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, '✅ Pessoa cadastrada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao cadastrar pessoa. Verifique os dados.')
        return super().form_invalid(form)

class PersonUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/person_form.html'
    success_url = reverse_lazy('person-list')
    
    def get_queryset(self):
        return Person.objects.filter(usuario=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Pessoa atualizada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao atualizar pessoa. Verifique os dados.')
        return super().form_invalid(form)

class PersonDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Person
    template_name = 'pages/confirm/person_confirm_delete.html'
    success_url = reverse_lazy('person-list')
    
    def get_queryset(self):
        return Person.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '✅ Pessoa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA COMPANY (EMPRESA)
# ===========================================

class CompanyListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'pages/lists/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10
    
    def get_queryset(self):
        return Company.objects.filter(usuario=self.request.user)

class CompanyDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'pages/detail/company_detail.html'
    context_object_name = 'company'
    
    def get_queryset(self):
        return Company.objects.filter(usuario=self.request.user)

class CompanyCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Company
    form_class = CompanyForm
    template_name = 'pages/forms/company_form.html'
    success_url = reverse_lazy('company-list')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, '✅ Empresa cadastrada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao cadastrar empresa. Verifique os dados.')
        return super().form_invalid(form)

class CompanyUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Company
    form_class = CompanyForm
    template_name = 'pages/forms/company_form.html'
    success_url = reverse_lazy('company-list')
    
    def get_queryset(self):
        return Company.objects.filter(usuario=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Empresa atualizada com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao atualizar empresa. Verifique os dados.')
        return super().form_invalid(form)

class CompanyDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'pages/confirm/company_confirm_delete.html'
    success_url = reverse_lazy('company-list')
    
    def get_queryset(self):
        return Company.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '✅ Empresa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA CONTRACT (CONTRATO)
# ===========================================

class ContractListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Contract
    template_name = 'pages/lists/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 10
    
    def get_queryset(self):
        return Contract.objects.filter(usuario=self.request.user)

class ContractDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Contract
    template_name = 'pages/detail/contract_detail.html'
    context_object_name = 'contract'
    
    def get_queryset(self):
        return Contract.objects.filter(usuario=self.request.user)

class ContractCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    success_url = reverse_lazy('contract-list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar choices para apenas empresas e pessoas do usuário atual
        form.fields['company'].queryset = Company.objects.filter(usuario=self.request.user)
        form.fields['person'].queryset = Person.objects.filter(usuario=self.request.user)
        return form
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, '✅ Contrato cadastrado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao cadastrar contrato. Verifique os dados.')
        return super().form_invalid(form)

class ContractUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    success_url = reverse_lazy('contract-list')
    
    def get_queryset(self):
        return Contract.objects.filter(usuario=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtrar choices para apenas empresas e pessoas do usuário atual
        form.fields['company'].queryset = Company.objects.filter(usuario=self.request.user)
        form.fields['person'].queryset = Person.objects.filter(usuario=self.request.user)
        return form
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Contrato atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao atualizar contrato. Verifique os dados.')
        return super().form_invalid(form)

class ContractDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = ["empresa_admin", "funcionario"]
    login_url = reverse_lazy('login')
    model = Contract
    template_name = 'pages/confirm/contract_confirm_delete.html'
    success_url = reverse_lazy('contract-list')
    
    def get_queryset(self):
        return Contract.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '✅ Contrato excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA STATE (ESTADO) - ADMIN ONLY
# ===========================================

class StateListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = "empresa_admin"
    login_url = reverse_lazy('login')
    model = State
    template_name = 'pages/lists/state_list.html'
    context_object_name = 'states'
    paginate_by = 10
    
    def get_queryset(self):
        return State.objects.all().order_by('name')

class StateCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = "empresa_admin"
    login_url = reverse_lazy('login')
    model = State
    form_class = StateForm
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Estado cadastrado com sucesso!')
        return super().form_valid(form)

class StateUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = "empresa_admin"
    login_url = reverse_lazy('login')
    model = State
    form_class = StateForm
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Estado atualizado com sucesso!')
        return super().form_valid(form)

class StateDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "empresa_admin"
    login_url = reverse_lazy('login')
    model = State
    template_name = 'pages/confirm/state_confirm_delete.html'
    success_url = reverse_lazy('state-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '✅ Estado excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA CITY (CIDADE) - ADMIN ONLY
# ===========================================

class CityListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = "empresa_admin"
    login_url = reverse_lazy('login')
    model = City
    template_name = 'pages/lists/city_list.html'
    context_object_name = 'cities'
    paginate_by = 10
    
    def get_queryset(self):
        return City.objects.all().order_by('name')

class CityCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = "empresa_admin"
    login_url = reverse_lazy('login')
    model = City
    form_class = CityForm
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Cidade cadastrada com sucesso!')
        return super().form_valid(form)

class CityUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = "empresa_admin"
    login_url = reverse_lazy('login')
    model = City
    form_class = CityForm
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, '✅ Cidade atualizada com sucesso!')
        return super().form_valid(form)

class CityDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "empresa_admin"
    login_url = reverse_lazy('login')
    model = City
    template_name = 'pages/confirm/city_confirm_delete.html'
    success_url = reverse_lazy('city-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, '✅ Cidade excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEW PARA HOME
# ===========================================

class HomeView(LoginRequiredMixin, TemplateView):
    """
    Dashboard principal com KPIs e registros recentes
    """
    login_url = reverse_lazy('login')
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Data de uma semana atrás para filtros
        uma_semana_atras = timezone.now() - timedelta(days=7)
        
        # KPIs principais - contagens totais
        context['total_pessoas'] = Person.objects.filter(usuario=user).count()
        context['total_empresas'] = Company.objects.filter(usuario=user).count() 
        context['total_contratos'] = Contract.objects.filter(usuario=user).count()
        
        # KPI da semana
        context['pessoas_ultima_semana'] = Person.objects.filter(
            usuario=user, 
            created_at__gte=uma_semana_atras
        ).count()
        
        # Para compatibilidade com templates existentes
        context['minhas_pessoas'] = context['total_pessoas']
        context['minhas_empresas'] = context['total_empresas'] 
        context['meus_contratos'] = context['total_contratos']
        
        # Listas de registros recentes (últimos 5)
        context['ultimas_pessoas'] = Person.objects.filter(usuario=user).order_by('-created_at')[:5]
        context['ultimas_empresas'] = Company.objects.filter(usuario=user).order_by('-created_at')[:5]
        context['ultimos_contratos'] = Contract.objects.filter(usuario=user).order_by('-created_at')[:5]
        
        # Dados adicionais para o dashboard
        context['contratos_ativos'] = Contract.objects.filter(
            usuario=user,
            is_active=True
        ).count()
        
        # Estatísticas mensais
        um_mes_atras = timezone.now() - timedelta(days=30)
        context['empresas_ultimo_mes'] = Company.objects.filter(
            usuario=user,
            created_at__gte=um_mes_atras
        ).count()
        
        context['contratos_ultimo_mes'] = Contract.objects.filter(
            usuario=user,
            created_at__gte=um_mes_atras
        ).count()
        
        return context

# ===========================================
# VIEW PARA PÁGINA INICIAL (INDEX)
# ===========================================

class IndexView(ListView):
    """View para página inicial (index)"""
    model = Person
    template_name = 'pages/index.html'
    context_object_name = 'recent_persons'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Person.objects.filter(usuario=self.request.user)[:3]
        return Person.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            context.update({
                'recent_companies': Company.objects.filter(usuario=user)[:3],
                'recent_contracts': Contract.objects.filter(usuario=user)[:3],
            })
        return context

class AboutView(ListView):
    """View para página sobre"""
    model = Person
    template_name = 'pages/about.html'
    context_object_name = 'persons'
    
    def get_queryset(self):
        return Person.objects.none()

# ADICIONAR AS VIEWS DE DETAIL QUE ESTÃO FALTANDO (se necessário)

class StateDetailView(GroupRequiredMixin, DetailView):
    """View para detalhar Estado (apenas empresa_admin)"""
    model = State
    template_name = 'pages/detail/state_detail.html'
    context_object_name = 'state'
    group_required = ['empresa_admin']

class CityDetailView(GroupRequiredMixin, DetailView):
    """View para detalhar Cidade (apenas empresa_admin)"""
    model = City
    template_name = 'pages/detail/city_detail.html'
    context_object_name = 'city'
    group_required = ['empresa_admin']

class ContractDetailView(LoginRequiredMixin, DetailView):
    """View para detalhar Contrato"""
    model = Contract
    template_name = 'pages/detail/contract_detail.html'
    context_object_name = 'contract'
    login_url = reverse_lazy('login')
    
    def get_queryset(self):
        return Contract.objects.filter(usuario=self.request.user)

class CompanyDetailView(LoginRequiredMixin, DetailView):
    """View para detalhar Empresa"""
    model = Company
    template_name = 'pages/detail/company_detail.html'
    context_object_name = 'company'
    login_url = reverse_lazy('login')
    
    def get_queryset(self):
        return Company.objects.filter(usuario=self.request.user)

class PersonDetailView(LoginRequiredMixin, DetailView):
    """View para detalhar Pessoa"""
    model = Person
    template_name = 'pages/detail/person_detail.html'
    context_object_name = 'person'
    login_url = reverse_lazy('login')
    
    def get_queryset(self):
        return Person.objects.filter(usuario=self.request.user)