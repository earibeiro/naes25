from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
)
from braces.views import GroupRequiredMixin
from .models import Person, Company, State, City, Contract
from .forms import PersonForm, CompanyForm, ContractForm, StateForm, CityForm

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

class HomeView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Person
    template_name = 'pages/home.html'
    context_object_name = 'recent_persons'
    
    def get_queryset(self):
        return Person.objects.filter(usuario=self.request.user)[:5]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context.update({
            'recent_companies': Company.objects.filter(usuario=user)[:5],
            'recent_contracts': Contract.objects.filter(usuario=user)[:5],
            'total_persons': Person.objects.filter(usuario=user).count(),
            'total_companies': Company.objects.filter(usuario=user).count(),
            'total_contracts': Contract.objects.filter(usuario=user).count(),
        })
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