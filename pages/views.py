from django.views.generic import TemplateView
from .models import State, City, Person, Company
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class MainPage(TemplateView):
    template_name = 'pages/index.html'

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class ProjectsView(TemplateView):
    template_name = 'pages/projects.html'

class ContactView(TemplateView):
    template_name = 'pages/contact.html'

class StateCreateView(CreateView):
    model = State
    fields = ['name', 'abbreviation']
    template_name = 'pages/state_form.html'
    success_url = reverse_lazy('index')

class CityCreateView(CreateView):
    model = City
    fields = ['name', 'state']
    template_name = 'pages/city_form.html'
    success_url = reverse_lazy('index')

class PersonCreateView(CreateView):
    model = Person
    fields = ['name', 'cpf', 'email', 'phone', 'city']
    template_name = 'pages/person_form.html'
    success_url = reverse_lazy('index')

class CompanyCreateView(CreateView):
    model = Company
    fields = ['name', 'cnpj', 'email', 'phone', 'city']
    template_name = 'pages/company_form.html'
    success_url = reverse_lazy('index')

class StateUpdateView(UpdateView):
    model = State
    fields = ['name', 'abbreviation']
    template_name = 'pages/state_form.html'
    success_url = reverse_lazy('index')

class CityUpdateView(UpdateView):
    model = City
    fields = ['name', 'state']
    template_name = 'pages/city_form.html'
    success_url = reverse_lazy('index')

class PersonUpdateView(UpdateView):
    model = Person
    fields = ['name', 'cpf', 'email', 'phone', 'city']
    template_name = 'pages/person_form.html'
    success_url = reverse_lazy('index')

class CompanyUpdateView(UpdateView):
    model = Company
    fields = ['name', 'cnpj', 'email', 'phone', 'city']
    template_name = 'pages/company_form.html'
    success_url = reverse_lazy('index')

class StateDeleteView(DeleteView):
    model = State
    template_name = 'pages/state_confirm_delete.html'
    success_url = reverse_lazy('index')

class CityDeleteView(DeleteView):
    model = City
    template_name = 'pages/city_confirm_delete.html'
    success_url = reverse_lazy('index')

class PersonDeleteView(DeleteView):
    model = Person
    template_name = 'pages/person_confirm_delete.html'
    success_url = reverse_lazy('index')

class CompanyDeleteView(DeleteView):
    model = Company
    template_name = 'pages/company_confirm_delete.html'
    success_url = reverse_lazy('index')