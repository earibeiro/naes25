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
    GroupRequiredMixin
)

# Tentar importar mixins existentes
try:
    from .mixins import GroupRequiredMixin
    MIXINS_AVAILABLE = True
except ImportError:
    MIXINS_AVAILABLE = False
    
    # Criar mixins básicos inline
    class GroupRequiredMixin:
        group_required = None
        
        def dispatch(self, request, *args, **kwargs):
            if self.group_required and not request.user.groups.filter(name=self.group_required).exists():
                raise PermissionDenied("Você não tem permissão para acessar esta página.")
            return super().dispatch(request, *args, **kwargs)
    
    class OwnerQuerysetMixin(LoginRequiredMixin):
        owner_field_name = "usuario"
        
        def get_queryset(self):
            qs = super().get_queryset()
            return qs.filter(**{self.owner_field_name: self.request.user})
    
    class OwnerObjectPermissionMixin(UserPassesTestMixin):
        owner_field_name = "usuario"
        
        def test_func(self):
            try:
                obj = self.get_object()
                owner = getattr(obj, self.owner_field_name, None)
                return owner == self.request.user
            except:
                return False
    
    class OwnerCreateMixin(LoginRequiredMixin):
        owner_field_name = "usuario"
        
        def form_valid(self, form):
            if hasattr(form.instance, self.owner_field_name):
                setattr(form.instance, self.owner_field_name, self.request.user)
            return super().form_valid(form)
    
    class AdminOnlyMixin(UserPassesTestMixin):
        def test_func(self):
            u = self.request.user
            return u.is_superuser or u.groups.filter(name="empresa_admin").exists()

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

# ===========================================
# VIEWS PARA PERSON (PESSOA)
# ===========================================

class PersonListView(OwnerQuerysetMixin, ListView):
    """ListView para pessoas com escopo por owner"""
    model = Person
    template_name = 'pages/lists/person_list.html'
    context_object_name = 'persons'
    paginate_by = 10

class PersonCreateView(OwnerCreateMixin, GroupRequiredMixin, CreateView):
    """CreateView para pessoas"""
    model = Person
    form_class = PersonForm  # ✅ USAR FORM CUSTOMIZADO
    template_name = 'pages/forms/person_form.html'
    success_url = reverse_lazy('person-list')
    group_required = 'funcionario'
    
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

class PersonDetailView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, DetailView):
    """DetailView para pessoas (apenas dono pode ver)"""
    model = Person
    template_name = 'pages/detail/person_detail.html'
    context_object_name = 'person'

class PersonUpdateView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, UpdateView):
    """UpdateView para pessoas (apenas dono pode editar)"""
    model = Person
    form_class = PersonForm  # ✅ USAR FORM CUSTOMIZADO
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

class PersonDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, DeleteView):
    """DeleteView para pessoas (apenas dono pode deletar)"""
    model = Person
    template_name = 'pages/delete/person_confirm_delete.html'
    success_url = reverse_lazy('person-list')
    
    def delete(self, request, *args, **kwargs):
        person_name = self.get_object().full_name  # ✅ CAMPO CORRETO
        messages.success(request, f'✅ Pessoa "{person_name}" excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA COMPANY (EMPRESA) - CORRIGIDAS
# ===========================================

class CompanyListView(OwnerQuerysetMixin, ListView):
    """ListView para empresas com escopo por owner"""
    model = Company
    template_name = 'pages/lists/company_list.html'
    context_object_name = 'companies'
    paginate_by = 10

class CompanyCreateView(OwnerCreateMixin, GroupRequiredMixin, CreateView):
    """CreateView para empresas"""
    model = Company
    form_class = CompanyForm  # ✅ USAR FORM CUSTOMIZADO
    template_name = 'pages/forms/company_form.html'
    success_url = reverse_lazy('company-list')
    group_required = 'funcionario'
    
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

class CompanyDetailView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, DetailView):
    """DetailView para empresas (apenas dono pode ver)"""
    model = Company
    template_name = 'pages/detail/company_detail.html'
    context_object_name = 'company'

class CompanyUpdateView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, UpdateView):
    """UpdateView para empresas (apenas dono pode editar)"""
    model = Company
    form_class = CompanyForm  # ✅ USAR FORM CUSTOMIZADO
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

class CompanyDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, DeleteView):
    """DeleteView para empresas (apenas dono pode deletar)"""
    model = Company
    template_name = 'pages/delete/company_confirm_delete.html'
    success_url = reverse_lazy('company-list')
    
    def delete(self, request, *args, **kwargs):
        company_name = self.get_object().corporate_name  # ✅ CAMPO CORRETO
        messages.success(request, f'✅ Empresa "{company_name}" excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS PARA CONTRACT (CONTRATO) - CORRIGIDAS
# ===========================================

class ContractListView(OwnerQuerysetMixin, ListView):
    """ListView para contratos com escopo por owner"""
    model = Contract
    template_name = 'pages/lists/contract_list.html'
    context_object_name = 'contracts'
    paginate_by = 10

class ContractCreateView(OwnerCreateMixin, CreateView):
    """CreateView para contratos"""
    model = Contract
    form_class = ContractForm  # Usar form customizado
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

class ContractDetailView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, DetailView):
    """DetailView para contratos (apenas dono pode ver)"""
    model = Contract
    template_name = 'pages/detail/contract_detail.html'
    context_object_name = 'contract'

class ContractUpdateView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, UpdateView):
    """UpdateView para contratos (apenas dono pode editar)"""
    model = Contract
    form_class = ContractForm  # Usar form customizado
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

class ContractDeleteView(OwnerQuerysetMixin, OwnerObjectPermissionMixin, DeleteView):
    """DeleteView para contratos (apenas dono pode deletar)"""
    model = Contract
    template_name = 'pages/delete/contract_confirm_delete.html'
    success_url = reverse_lazy('contract-list')
    
    def delete(self, request, *args, **kwargs):
        contract_title = self.get_object().title
        messages.success(request, f'✅ Contrato "{contract_title}" excluído com sucesso!')
        return super().delete(request, *args, **kwargs)

# ===========================================
# VIEWS ADMINISTRATIVAS (ESTADOS E CIDADES)
# ===========================================

class StateListView(AdminOnlyMixin, ListView):
    """ListView para estados (apenas admin)"""
    model = State
    template_name = 'pages/lists/state_list.html'
    context_object_name = 'states'
    paginate_by = 50

class StateCreateView(AdminOnlyMixin, CreateView):
    """CreateView para estados (apenas admin)"""
    model = State
    fields = '__all__'
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')

class StateUpdateView(AdminOnlyMixin, UpdateView):
    """UpdateView para estados (apenas admin)"""
    model = State
    fields = '__all__'
    template_name = 'pages/forms/state_form.html'
    success_url = reverse_lazy('state-list')

class StateDeleteView(AdminOnlyMixin, DeleteView):
    """DeleteView para estados (apenas admin)"""
    model = State
    template_name = 'pages/delete/state_confirm_delete.html'
    success_url = reverse_lazy('state-list')

class CityListView(AdminOnlyMixin, ListView):
    """ListView para cidades (apenas admin)"""
    model = City
    template_name = 'pages/lists/city_list.html'
    context_object_name = 'cities'
    paginate_by = 50

class CityCreateView(AdminOnlyMixin, CreateView):
    """CreateView para cidades (apenas admin)"""
    model = City
    fields = '__all__'
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')

class CityUpdateView(AdminOnlyMixin, UpdateView):
    """UpdateView para cidades (apenas admin)"""
    model = City
    fields = '__all__'
    template_name = 'pages/forms/city_form.html'
    success_url = reverse_lazy('city-list')

class CityDeleteView(AdminOnlyMixin, DeleteView):
    """DeleteView para cidades (apenas admin)"""
    model = City
    template_name = 'pages/delete/city_confirm_delete.html'
    success_url = reverse_lazy('city-list')

# ===========================================
# VIEWS DE FLUXO DE RASCUNHO E HOME
# ===========================================

class HomeView(LoginRequiredMixin, TemplateView):
    """Dashboard principal com KPIs e registros recentes"""
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

class IndexView(TemplateView):
    """Página inicial pública"""
    template_name = 'pages/index.html'

class AboutView(TemplateView):
    """Página sobre o sistema"""
    template_name = 'pages/about.html'

# ===========================================
# VIEWS DE FLUXO DE RASCUNHO ANÔNIMO
# ===========================================

class ContratoDraftStartView(FormView):
    """View para iniciar rascunho de contrato anônimo"""
    template_name = 'pages/contratos/contrato_draft_form.html'
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
            messages.info(request, 'Faça login ou crie uma conta para finalizar seu contrato.')
            # Redireciona para escolha de cadastro com next
            return redirect(f"{reverse('usuarios:cadastro-escolha')}?next={reverse('contrato-draft-finalize')}")
        
        # Usuário autenticado - cria contrato real
        return self.finalize_contract(request)
    
    def finalize_contract(self, request):
        draft = request.session.get('draft_contrato', {})
        
        try:
            # Cria empresa se fornecida e não existir
            company = None
            if draft.get('empresa_nome'):
                company, created = Company.objects.get_or_create(
                    corporate_name=draft['empresa_nome'],  # ✅ CAMPO CORRETO
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