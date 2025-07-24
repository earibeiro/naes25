from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.views.generic import TemplateView
from .models import State, City, Person, Company
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import PersonForm, CompanyForm, StateForm, CityForm
from django.contrib import messages

# Páginas principais (públicas - SEM proteção)
class MainPage(TemplateView):
    template_name = 'pages/index.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class ProjectsView(TemplateView):
    template_name = 'pages/projects.html'

class ContactView(TemplateView):
    template_name = 'pages/contact.html'

# CRUD States (APENAS ADMINISTRADORES)
class StateCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = State
    form_class = StateForm 
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Estado cadastrado com sucesso!')
        return super().form_valid(form)

class StateUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = State
    form_class = StateForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Estado atualizado com sucesso!')
        return super().form_valid(form)

class StateDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = State
    template_name = 'pages/confirmations/delete_confirm.html'
    success_url = reverse_lazy('state-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Estado excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

class StateListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = State
    template_name = 'pages/listas/state_list.html'
    context_object_name = 'states'
    paginate_by = 10

class StateDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = State
    template_name = 'pages/detalhes/state_detail.html'
    context_object_name = 'state'

# CRUD Cities (APENAS ADMINISTRADORES)
class CityCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = City
    form_class = CityForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cidade cadastrada com sucesso!')
        return super().form_valid(form)

class CityUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = City
    form_class = CityForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cidade atualizada com sucesso!')
        return super().form_valid(form)

class CityDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = City
    template_name = 'pages/confirmations/delete_confirm.html'
    success_url = reverse_lazy('city-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cidade excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

class CityListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = City
    template_name = 'pages/listas/city_list.html'
    context_object_name = 'cities'
    paginate_by = 10

class CityDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = "Administrador"
    login_url = reverse_lazy('login')
    model = City
    template_name = 'pages/detalhes/city_detail.html'
    context_object_name = 'city'

# CRUD Persons (USUÁRIOS E ADMINISTRADORES)
class PersonCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = ["Administrador", "Usuarios"]
    login_url = reverse_lazy('login')
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('person-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Pessoa cadastrada com sucesso!')
        return super().form_valid(form)

class PersonUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ["Administrador", "Usuarios"]
    login_url = reverse_lazy('login')
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('person-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Pessoa atualizada com sucesso!')
        return super().form_valid(form)

class PersonDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "Administrador"  # Só admin pode excluir
    login_url = reverse_lazy('login')
    model = Person
    template_name = 'pages/confirmations/delete_confirm.html'
    success_url = reverse_lazy('person-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Pessoa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

class PersonListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = ["Administrador", "Usuarios"]
    login_url = reverse_lazy('login')
    model = Person
    template_name = 'pages/listas/person_list.html'
    context_object_name = 'persons'
    paginate_by = 10

class PersonDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = ["Administrador", "Usuarios"]
    login_url = reverse_lazy('login')
    model = Person
    template_name = 'pages/detalhes/person_detail.html'
    context_object_name = 'person'

# CRUD Companies (USUÁRIOS E ADMINISTRADORES)
class CompanyCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = ["Administrador", "Usuarios"]
    login_url = reverse_lazy('login')
    model = Company
    form_class = CompanyForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('company-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Empresa cadastrada com sucesso!')
        return super().form_valid(form)

class CompanyUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ["Administrador", "Usuarios"]
    login_url = reverse_lazy('login')
    model = Company
    form_class = CompanyForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('company-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Empresa atualizada com sucesso!')
        return super().form_valid(form)

class CompanyDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "Administrador"  # Só admin pode excluir
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'pages/confirmations/delete_confirm.html'
    success_url = reverse_lazy('company-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Empresa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

class CompanyListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = ["Administrador", "Usuarios"]
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'pages/listas/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10

class CompanyDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = ["Administrador", "Usuarios"]
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'pages/detalhes/company_detail.html'
    context_object_name = 'company'