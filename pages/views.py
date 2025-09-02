# IMPORTS SEGUROS
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, FormView, View
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

# ===========================================
# VIEWS PARA PERSON (PESSOA) - COM PROTEÇÃO
# ===========================================

class PersonListView(OwnerQuerysetMixin, FuncionarioRequiredMixin, ListView):
    """ListView para pessoas - requer grupo funcionario"""
    model = Person
    template_name = 'pages/lists/person_list.html'
    context_object_name = 'persons'
    paginate_by = 10

class PersonCreateView(OwnerCreateMixin, FuncionarioRequiredMixin, CreateView):
    """CreateView para pessoas - requer grupo funcionario"""
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/person_form.html'
    success_url = reverse_lazy('person-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
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

class PersonUpdateView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, UpdateView):
    """UpdateView para pessoas - requer grupo funcionario + ownership"""
    model = Person
    form_class = PersonForm
    template_name = 'pages/forms/person_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Pessoa "{form.instance.full_name}" atualizada com sucesso!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('person-detail', kwargs={'pk': self.object.pk})

class PersonDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DeleteView):
    """DeleteView para pessoas - requer grupo funcionario + ownership"""
    model = Person
    template_name = 'pages/delete/person_confirm_delete.html'
    success_url = reverse_lazy('person-list')
    
    def delete(self, request, *args, **kwargs):
        person_name = self.get_object().full_name
        messages.success(request, f'✅ Pessoa "{person_name}" excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA COMPANY (EMPRESA) - COM PROTEÇÃO
# ===========================================

class CompanyListView(OwnerQuerysetMixin, FuncionarioRequiredMixin, ListView):
    """ListView para empresas - requer grupo funcionario"""
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
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Empresa "{form.instance.corporate_name}" atualizada com sucesso!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('company-detail', kwargs={'pk': self.object.pk})

class CompanyDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DeleteView):
    """DeleteView para empresas - requer grupo funcionario + ownership"""
    model = Company
    template_name = 'pages/delete/company_confirm_delete.html'
    success_url = reverse_lazy('company-list')
    
    def delete(self, request, *args, **kwargs):
        company_name = self.get_object().corporate_name
        messages.success(request, f'✅ Empresa "{company_name}" excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA CONTRACT (CONTRATO) - COM PROTEÇÃO
# ===========================================

class ContractListView(OwnerQuerysetMixin, FuncionarioRequiredMixin, ListView):
    """ListView para contratos - requer grupo funcionario"""
    model = Contract
    template_name = 'pages/lists/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 10

class ContractCreateView(OwnerCreateMixin, FuncionarioRequiredMixin, CreateView):
    """CreateView para contratos - requer grupo funcionario"""
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    success_url = reverse_lazy('contract-list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
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
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Contrato "{form.instance.title}" atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao atualizar contrato. Verifique os dados.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('contract-detail', kwargs={'pk': self.object.pk})

class ContractDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, FuncionarioRequiredMixin, DeleteView):
    """DeleteView para contratos - requer grupo funcionario + ownership"""
    model = Contract
    template_name = 'pages/delete/contract_confirm_delete.html'
    success_url = reverse_lazy('contract-list')
    
    def delete(self, request, *args, **kwargs):
        contract_title = self.get_object().title
        messages.success(request, f'✅ Contrato "{contract_title}" excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS ADMINISTRATIVAS (APENAS ADMIN) - PROTEÇÃO DUPLA
# ===========================================

class StateListView(AdminRequiredMixin, ListView):
    """ListView para estados - APENAS empresa_admin"""
    model = State
    template_name = 'pages/lists/state_list.html'
    context_object_name = 'states'
    paginate_by = 50

class StateCreateView(AdminRequiredMixin, CreateView):
    """CreateView para estados - APENAS empresa_admin"""
    model = State
    fields = '__all__'
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Estado "{form.instance.name}" criado com sucesso!')
        return super().form_valid(form)

class StateUpdateView(AdminRequiredMixin, UpdateView):
    """UpdateView para estados - APENAS empresa_admin"""
    model = State
    fields = '__all__'
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Estado "{form.instance.name}" atualizado com sucesso!')
        return super().form_valid(form)

class StateDeleteView(AdminRequiredMixin, DeleteView):
    """DeleteView para estados - APENAS empresa_admin"""
    model = State
    template_name = 'pages/delete/state_confirm_delete.html'
    success_url = reverse_lazy('state-list')
    
    def delete(self, request, *args, **kwargs):
        state_name = self.get_object().name
        messages.success(request, f'✅ Estado "{state_name}" excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

class CityListView(AdminRequiredMixin, ListView):
    """ListView para cidades - APENAS empresa_admin"""
    model = City
    template_name = 'pages/lists/city_list.html'
    context_object_name = 'cities'
    paginate_by = 50

class CityCreateView(AdminRequiredMixin, CreateView):
    """CreateView para cidades - APENAS empresa_admin"""
    model = City
    fields = '__all__'
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Cidade "{form.instance.name}" criada com sucesso!')
        return super().form_valid(form)

class CityUpdateView(AdminRequiredMixin, UpdateView):
    """UpdateView para cidades - APENAS empresa_admin"""
    model = City
    fields = '__all__'
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')
    
    def form_valid(self, form):
        messages.success(self.request, f'✅ Cidade "{form.instance.name}" atualizada com sucesso!')
        return super().form_valid(form)

class CityDeleteView(AdminRequiredMixin, DeleteView):
    """DeleteView para cidades - APENAS empresa_admin"""
    model = City
    template_name = 'pages/delete/city_confirm_delete.html'
    success_url = reverse_lazy('city-list')
    
    def delete(self, request, *args, **kwargs):
        city_name = self.get_object().name
        messages.success(request, f'✅ Cidade "{city_name}" excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS HÍBRIDAS - RASCUNHOS (ANÔNIMO + FUNCIONARIO)
# ===========================================

class ContratoDraftStartView(FormView):
    """View para iniciar rascunho - PERMITE ANÔNIMO"""
    template_name = 'pages/contratos/contrato_draft_form.html'
    success_url = reverse_lazy('contrato-draft-review')
    
    # Não requer grupo - permite acesso anônimo
    
    def get_form_class(self):
        """Cria form dinamicamente para evitar dependências"""
        from django import forms
        
        class ContratoDraftForm(forms.Form):
            titulo = forms.CharField(
                max_length=200,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Ex: Contrato de Prestação de Serviços'
                })
            )
            descricao = forms.CharField(
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Descreva os termos do contrato...'
                })
            )
            empresa_nome = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Nome da empresa (opcional)'
                })
            )
        
        return ContratoDraftForm
    
    def form_valid(self, form):
        # Salva dados na sessão
        self.request.session['draft_contrato'] = {
            'titulo': form.cleaned_data['titulo'],
            'descricao': form.cleaned_data['descricao'],
            'empresa_nome': form.cleaned_data.get('empresa_nome', ''),
            'created_at': timezone.now().isoformat()
        }
        
        if self.request.user.is_authenticated:
            messages.success(self.request, '✅ Rascunho salvo! Revise antes de finalizar.')
        else:
            messages.info(self.request, 'ℹ️ Rascunho criado! Você precisará fazer login para finalizar.')
            
        return super().form_valid(form)

class ContratoDraftReviewView(TemplateView):
    """View para revisar rascunho - PERMITE ANÔNIMO"""
    template_name = 'pages/contratos/contrato_draft_review.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft = self.request.session.get('draft_contrato', {})
        context['draft'] = draft
        
        if not draft:
            messages.warning(self.request, '⚠️ Nenhum rascunho encontrado. Comece um novo contrato.')
        
        return context

class ContratoDraftFinalizeView(FuncionarioRequiredMixin, View):
    """View para finalizar rascunho - REQUER FUNCIONARIO"""
    
    def get(self, request):
        # Verifica se há draft na sessão
        if 'draft_contrato' not in request.session:
            messages.error(request, '❌ Nenhum rascunho encontrado.')
            return redirect('contrato-draft-start')
        
        # Usuário autenticado com grupo correto - cria contrato real
        return self.finalize_contract(request)
    
    def finalize_contract(self, request):
        draft = request.session.get('draft_contrato', {})
        
        try:
            # Cria empresa se fornecida e não existir
            company = None
            if draft.get('empresa_nome'):
                company, created = Company.objects.get_or_create(
                    corporate_name=draft['empresa_nome'],
                    usuario=request.user,
                    defaults={
                        'trade_name': draft['empresa_nome'],
                        'email': '',
                        'phone': '',
                        'address': '',
                        'city': None,
                        'data_processing_purpose': f"Empresa criada via rascunho: {draft['empresa_nome']}"
                    }
                )
                
                if created:
                    messages.info(request, f'ℹ️ Empresa "{company.corporate_name}" criada automaticamente.')
            
            # Cria contrato
            contract = Contract.objects.create(
                title=draft['titulo'],
                description=draft['descricao'],
                company=company,
                person=None,
                usuario=request.user,
                data_processing_purpose=f"Contrato: {draft['titulo']}",
                is_active=True
            )
            
            # Limpa sessão
            del request.session['draft_contrato']
            if 'draft_next' in request.session:
                del request.session['draft_next']
            
            messages.success(request, f'✅ Contrato "{contract.title}" criado com sucesso!')
            return redirect('contract-detail', pk=contract.pk)
            
        except Exception as e:
            messages.error(request, f'❌ Erro ao criar contrato: {str(e)}')
            return redirect('contrato-draft-start')