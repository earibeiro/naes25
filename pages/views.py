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

# IMPORTAR FORMS COM TRATAMENTO DE ERRO
try:
    from .forms import PersonForm, CompanyForm, ContractForm, StateForm, CityForm
except ImportError:
    # Se não existirem, criar forms básicos
    from django import forms
    
    class PersonForm(forms.ModelForm):
        class Meta:
            model = Person
            fields = '__all__'
            exclude = ['usuario']
    
    class CompanyForm(forms.ModelForm):
        class Meta:
            model = Company
            fields = '__all__'
            exclude = ['usuario']
    
    class ContractForm(forms.ModelForm):
        class Meta:
            model = Contract
            fields = '__all__'
            exclude = ['usuario']

# Importar mixins
try:
    from .mixins import GroupRequiredMixin
except ImportError:
    class GroupRequiredMixin:
        group_required = None
        
        def dispatch(self, request, *args, **kwargs):
            if self.group_required and not request.user.groups.filter(name=self.group_required).exists():
                raise PermissionDenied("Você não tem permissão para acessar esta página.")
            return super().dispatch(request, *args, **kwargs)

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

class ContractListView(LoginRequiredMixin, ListView):
    """ListView para contratos com escopo por owner"""
    model = Contract
    template_name = 'pages/lists/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 10
    login_url = reverse_lazy('login')
    
    def get_queryset(self):
        return Contract.objects.filter(
            usuario=self.request.user
        ).order_by('-created_at')

class ContractCreateView(LoginRequiredMixin, CreateView):
    """CreateView para contratos"""
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    login_url = reverse_lazy('login')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        # Se não tiver data de início, usar hoje
        if not form.instance.start_date:
            form.instance.start_date = timezone.now().date()
        messages.success(self.request, f'✅ Contrato "{form.instance.title}" criado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '❌ Erro ao criar contrato. Verifique os dados.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('contract-detail', kwargs={'pk': self.object.pk})

class ContractUpdateView(LoginRequiredMixin, UpdateView):
    """UpdateView para contratos (apenas dono pode editar)"""
    model = Contract
    form_class = ContractForm
    template_name = 'pages/forms/contract_form.html'
    login_url = reverse_lazy('login')
    
    def get_queryset(self):
        return Contract.objects.filter(usuario=self.request.user)
    
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

class ContractDetailView(LoginRequiredMixin, DetailView):
    """DetailView para contratos (apenas dono pode ver)"""
    model = Contract
    template_name = 'pages/detail/contract_detail.html'
    context_object_name = 'contract'
    login_url = reverse_lazy('login')
    
    def get_queryset(self):
        return Contract.objects.filter(usuario=self.request.user)

class ContractDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """DeleteView para contratos (apenas dono pode deletar)"""
    model = Contract
    template_name = 'pages/delete/contract_confirm_delete.html'
    success_url = reverse_lazy('contract-list')
    login_url = reverse_lazy('login')
    
    def test_func(self):
        """Verifica se o usuário é o dono do contrato"""
        try:
            obj = self.get_object()
            return obj.usuario == self.request.user
        except:
            return False
    
    def get_queryset(self):
        return Contract.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        contract_title = self.get_object().title
        messages.success(request, f'✅ Contrato "{contract_title}" excluído com sucesso!')
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
        
        # KPIs principais - contagens totais (com try/except para segurança)
        try:
            context['total_pessoas'] = Person.objects.filter(usuario=user).count()
        except:
            context['total_pessoas'] = 0
            
        try:
            context['total_empresas'] = Company.objects.filter(usuario=user).count()
        except:
            context['total_empresas'] = 0
            
        try:
            context['total_contratos'] = Contract.objects.filter(usuario=user).count()
        except:
            context['total_contratos'] = 0
        
        # KPI da semana
        try:
            context['pessoas_ultima_semana'] = Person.objects.filter(
                usuario=user, 
                created_at__gte=uma_semana_atras
            ).count()
        except:
            context['pessoas_ultima_semana'] = 0
        
        # Para compatibilidade com templates existentes
        context['minhas_pessoas'] = context['total_pessoas']
        context['minhas_empresas'] = context['total_empresas'] 
        context['meus_contratos'] = context['total_contratos']
        
        # Listas de registros recentes (últimos 5)
        try:
            context['ultimas_pessoas'] = Person.objects.filter(usuario=user).order_by('-created_at')[:5]
        except:
            context['ultimas_pessoas'] = []
            
        try:
            context['ultimas_empresas'] = Company.objects.filter(usuario=user).order_by('-created_at')[:5]
        except:
            context['ultimas_empresas'] = []
            
        try:
            context['ultimos_contratos'] = Contract.objects.filter(usuario=user).order_by('-created_at')[:5]
        except:
            context['ultimos_contratos'] = []
        
        # Contratos ativos (usando campo is_active se existir)
        try:
            context['contratos_ativos'] = Contract.objects.filter(
                usuario=user, 
                is_active=True
            ).count()
        except:
            # Fallback se campo não existir
            context['contratos_ativos'] = context['total_contratos']
        
        # Estatísticas mensais
        um_mes_atras = timezone.now() - timedelta(days=30)
        try:
            context['empresas_ultimo_mes'] = Company.objects.filter(
                usuario=user,
                created_at__gte=um_mes_atras
            ).count()
        except:
            context['empresas_ultimo_mes'] = 0
        
        try:
            context['contratos_ultimo_mes'] = Contract.objects.filter(
                usuario=user,
                created_at__gte=um_mes_atras
            ).count()
        except:
            context['contratos_ultimo_mes'] = 0
        
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

from django.shortcuts import redirect
from django.contrib import messages

class ContratoDraftStartView(FormView):
    """View para iniciar rascunho de contrato anônimo"""
    template_name = 'pages/contratos/contrato_draft_form.html'
    form_class = None  # Vamos criar um form simples
    success_url = reverse_lazy('contrato-draft-review')
    
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
        return super().form_valid(form)

class ContratoDraftReviewView(TemplateView):
    """View para revisar rascunho de contrato"""
    template_name = 'pages/contratos/contrato_draft_review.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft = self.request.session.get('draft_contrato', {})
        context['draft'] = draft
        return context

class ContratoDraftFinalizeView(View):
    """View para finalizar rascunho e criar contrato real"""
    
    def get(self, request):
        # Verifica se há draft na sessão
        if 'draft_contrato' not in request.session:
            messages.error(request, 'Nenhum rascunho encontrado.')
            return redirect('contrato-draft-start')
        
        if not request.user.is_authenticated:
            # Salva intenção de finalizar após login
            request.session['draft_next'] = 'finalize'
            messages.info(request, 'Faça login para finalizar seu contrato.')
            return redirect(f"{reverse('login')}?next={reverse('contrato-draft-finalize')}")
        
        # Usuário autenticado - cria contrato real
        return self.finalize_contract(request)
    
    def finalize_contract(self, request):
        draft = request.session.get('draft_contrato', {})
        
        try:
            # Cria empresa se fornecida e não existir
            company = None
            if draft.get('empresa_nome'):
                company, created = Company.objects.get_or_create(
                    nome=draft['empresa_nome'],
                    usuario=request.user,
                    defaults={
                        'email': '',
                        'telefone': '',
                        'cidade': None
                    }
                )
            
            # Cria contrato
            contract = Contract.objects.create(
                title=draft['titulo'],
                description=draft['descricao'],
                company=company,
                person=None,  # Pode ser adicionado depois
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