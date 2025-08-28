from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.views.generic import TemplateView
from .models import State, City, Person, Company
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import PersonForm, CompanyForm, StateForm, CityForm
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta

# Páginas principais (públicas - SEM proteção)
class MainPage(TemplateView):
    template_name = 'pages/main.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class ProjectsView(TemplateView):
    template_name = 'pages/projects.html'

class ContactView(TemplateView):
    template_name = 'pages/contact.html'

class HomeView(TemplateView):
    template_name = 'pages/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contadores gerais
        context['total_pessoas'] = Person.objects.count()
        context['total_empresas'] = Company.objects.count()
        context['total_estados'] = State.objects.count()
        context['total_cidades'] = City.objects.count()
        
        # Contadores do usuário logado (se autenticado)
        if self.request.user.is_authenticated:
            context['minhas_pessoas'] = Person.objects.filter(usuario=self.request.user).count()
            context['minhas_empresas'] = Company.objects.filter(usuario=self.request.user).count()
            
            # Highlights - Últimos registros do usuário
            context['ultimas_pessoas'] = Person.objects.filter(
                usuario=self.request.user
            ).order_by('-consent_date')[:5]
            
            context['ultimas_empresas'] = Company.objects.filter(
                usuario=self.request.user
            ).order_by('-consent_date')[:5]
            
            # Estatísticas adicionais
            context['pessoas_ultima_semana'] = Person.objects.filter(
                usuario=self.request.user,
                consent_date__gte=timezone.now() - timedelta(days=7)
            ).count()
            
            context['empresas_ultima_semana'] = Company.objects.filter(
                usuario=self.request.user,
                consent_date__gte=timezone.now() - timedelta(days=7)
            ).count()
        
        # Dados globais para todos os usuários
        context['pessoas_recentes_geral'] = Person.objects.order_by('-consent_date')[:3]
        context['empresas_recentes_geral'] = Company.objects.order_by('-consent_date')[:3]
        
        return context

# CRUD States (APENAS empresa_admin)
class StateCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = "empresa_admin"  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = State
    form_class = StateForm 
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Estado cadastrado com sucesso!')
        return super().form_valid(form)

class StateUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = "empresa_admin"  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = State
    form_class = StateForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Estado atualizado com sucesso!')
        return super().form_valid(form)

class StateDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "empresa_admin"  
    login_url = reverse_lazy('login')
    model = State
    template_name = 'pages/confirmations/delete_confirm.html'
    success_url = reverse_lazy('state-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Estado excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

class StateListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = "empresa_admin"
    login_url = reverse_lazy('login')
    model = State
    template_name = 'pages/lists/state_list.html' 
    context_object_name = 'states'
    paginate_by = 10

class StateDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = "empresa_admin"  
    login_url = reverse_lazy('login')
    model = State
    template_name = 'pages/detalhes/state_detail.html'
    context_object_name = 'state'

# CRUD Cities (APENAS empresa_admin)
class CityCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = "empresa_admin"  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = City
    form_class = CityForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cidade cadastrada com sucesso!')
        return super().form_valid(form)

class CityUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = "empresa_admin"  
    login_url = reverse_lazy('login')
    model = City
    form_class = CityForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cidade atualizada com sucesso!')
        return super().form_valid(form)

class CityDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "empresa_admin"  
    login_url = reverse_lazy('login')
    model = City
    template_name = 'pages/confirmations/delete_confirm.html'
    success_url = reverse_lazy('city-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cidade excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

class CityListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = "empresa_admin"  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = City
    template_name = 'pages/listas/city_list.html'
    context_object_name = 'cities'
    paginate_by = 10

class CityDetailView(GroupRequiredMixin, LoginRequiredMixin, DetailView):
    group_required = "empresa_admin"  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = City
    template_name = 'pages/detalhes/city_detail.html'
    context_object_name = 'city'

# CRUD Persons (empresa_admin E funcionario)
class PersonCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = ["empresa_admin", "funcionario"]  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('person-list')
    
    def form_valid(self, form):
        # ATRIBUIR OWNER: Define o usuário logado como owner
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Pessoa cadastrada com sucesso!')
        return super().form_valid(form)

class PersonUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ["empresa_admin", "funcionario"]  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('person-list')
    
    # ESCOPO POR OWNER: Só permite editar registros próprios
    def get_queryset(self):
        return Person.objects.filter(usuario=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Pessoa atualizada com sucesso!')
        return super().form_valid(form)

class PersonDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "empresa_admin"  # ATUALIZADO - Só admin pode excluir
    login_url = reverse_lazy('login')
    model = Person
    template_name = 'pages/confirmations/delete_confirm.html'
    success_url = reverse_lazy('person-list')
    
    # ESCOPO POR OWNER: Só permite excluir registros próprios
    def get_queryset(self):
        return Person.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Pessoa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

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
    group_required = ["empresa_admin", "funcionario"]  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = Person
    template_name = 'pages/detalhes/person_detail.html'
    context_object_name = 'person'
    
    # ESCOPO POR OWNER: Só mostra registros do usuário logado
    def get_queryset(self):
        return Person.objects.filter(usuario=self.request.user)

# CRUD Companies (empresa_admin E funcionario)
class CompanyCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = ["empresa_admin", "funcionario"]  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = Company
    form_class = CompanyForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('company-list')
    
    def form_valid(self, form):
        # ATRIBUIR OWNER: Define o usuário logado como owner
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Empresa cadastrada com sucesso!')
        return super().form_valid(form)

class CompanyUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = ["empresa_admin", "funcionario"]  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = Company
    form_class = CompanyForm
    template_name = 'pages/forms/forms.html'
    success_url = reverse_lazy('company-list')
    
    # ESCOPO POR OWNER: Só permite editar registros próprios
    def get_queryset(self):
        return Company.objects.filter(usuario=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Empresa atualizada com sucesso!')
        return super().form_valid(form)

class CompanyDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    group_required = "empresa_admin"  # ATUALIZADO - Só admin pode excluir
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'pages/confirmations/delete_confirm.html'
    success_url = reverse_lazy('company-list')
    
    # ESCOPO POR OWNER: Só permite excluir registros próprios
    def get_queryset(self):
        return Company.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Empresa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

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
    group_required = ["empresa_admin", "funcionario"]  # ATUALIZADO
    login_url = reverse_lazy('login')
    model = Company
    template_name = 'pages/detalhes/company_detail.html'
    context_object_name = 'company'
    
    # ESCOPO POR OWNER: Só permite ver registros próprios
    def get_queryset(self):
        return Company.objects.filter(usuario=self.request.user)