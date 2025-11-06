"""
Filtros usando django-filter para as ListViews
"""
import django_filters as df
from django import forms
from .models import Contract, Company, Person, State, City  # ✅ ADICIONAR State, City


class ContractFilter(df.FilterSet):
    """
    Filtro para contratos com campos de busca por:
    - Número do contrato
    - Nome da pessoa
    - Nome da empresa
    - Status ativo/inativo
    - Data de criação/vencimento
    """
    numero = df.CharFilter(
        field_name="numero_contrato",
        lookup_expr="icontains",
        label="Número do Contrato",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por número...'
        })
    )
    
    pessoa = df.CharFilter(
        field_name="person__full_name",
        lookup_expr="icontains",
        label="Nome da Pessoa",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por pessoa...'
        })
    )
    
    empresa = df.CharFilter(
        field_name="company__company_name",
        lookup_expr="icontains",
        label="Nome da Empresa",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por empresa...'
        })
    )
    
    is_active = df.BooleanFilter(
        field_name="is_active",
        label="Contrato Ativo",
        widget=forms.Select(
            choices=[
                ('', 'Todos'),
                ('true', 'Ativos'),
                ('false', 'Inativos')
            ],
            attrs={'class': 'form-select'}
        )
    )
    
    criado_de = df.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Criado A Partir De",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    criado_ate = df.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Criado Até",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    # ✅ REMOVER vencimento_de e vencimento_ate (campo não existe no modelo)
    # O modelo tem start_date e end_date
    
    inicio_de = df.DateFilter(
        field_name="start_date",
        lookup_expr="gte",
        label="Início A Partir De",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    inicio_ate = df.DateFilter(
        field_name="start_date",
        lookup_expr="lte",
        label="Início Até",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fim_de = df.DateFilter(
        field_name="end_date",
        lookup_expr="gte",
        label="Fim A Partir De",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fim_ate = df.DateFilter(
        field_name="end_date",
        lookup_expr="lte",
        label="Fim Até",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    class Meta:
        model = Contract
        fields = ["numero", "pessoa", "empresa", "is_active", "criado_de", "criado_ate", "inicio_de", "inicio_ate", "fim_de", "fim_ate"]


class CompanyFilter(df.FilterSet):
    """
    Filtro para empresas com campos de busca por:
    - Razão Social (icontains)
    - CNPJ (icontains)
    - Cidade (icontains)
    - Data de criação (gte/lte)
    """
    razao_social = df.CharFilter(
        field_name="company_name",
        lookup_expr="icontains",
        label="Razão Social",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por razão social...'
        })
    )
    
    cnpj = df.CharFilter(
        field_name="cnpj",
        lookup_expr="icontains",
        label="CNPJ",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por CNPJ...'
        })
    )
    
    cidade = df.CharFilter(
        field_name="city__name",
        lookup_expr="icontains",
        label="Cidade",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por cidade...'
        })
    )
    
    criada_de = df.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Criada A Partir De",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    criada_ate = df.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Criada Até",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    class Meta:
        model = Company
        fields = ["razao_social", "cnpj", "cidade", "criada_de", "criada_ate"]


class PersonFilter(df.FilterSet):
    """
    Filtro para pessoas com campos de busca por:
    - Nome (icontains)
    - CPF (icontains)
    - Cidade (icontains)
    - Data de criação (gte/lte)
    """
    nome = df.CharFilter(
        field_name="full_name",
        lookup_expr="icontains",
        label="Nome Completo",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome...'
        })
    )
    
    cpf = df.CharFilter(
        field_name="cpf",
        lookup_expr="icontains",
        label="CPF",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por CPF...'
        })
    )
    
    cidade = df.CharFilter(
        field_name="city__name",
        lookup_expr="icontains",
        label="Cidade",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por cidade...'
        })
    )
    
    criada_de = df.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Criada A Partir De",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    criada_ate = df.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Criada Até",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    class Meta:
        model = Person
        fields = ["nome", "cpf", "cidade", "criada_de", "criada_ate"]


# ✅ FILTROS DE STATE E CITY (COPIADOS DA RESPOSTA ANTERIOR)

class StateFilter(df.FilterSet):
    """
    Filtro para estados com campos de busca por:
    - Nome do estado (icontains)
    - Sigla (icontains)
    """
    nome = df.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Nome do Estado",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome do estado...'
        })
    )
    
    sigla = df.CharFilter(
        field_name="abbreviation",
        lookup_expr="icontains",
        label="Sigla (UF)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: SP, RJ, MG...',
            'maxlength': '2'
        })
    )
    
    class Meta:
        model = State
        fields = ["nome", "sigla"]


class CityFilter(df.FilterSet):
    """
    Filtro para cidades com campos de busca por:
    - Nome da cidade (icontains)
    - Estado (FK)
    """
    nome = df.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        label="Nome da Cidade",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome da cidade...'
        })
    )
    
    estado = df.ModelChoiceFilter(
        field_name="state",
        queryset=State.objects.all().order_by('name'),
        label="Estado",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    estado_sigla = df.CharFilter(
        field_name="state__abbreviation",
        lookup_expr="iexact",
        label="Sigla do Estado",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: SP',
            'maxlength': '2'
        })
    )
    
    class Meta:
        model = City
        fields = ["nome", "estado", "estado_sigla"]
# Deploy: 2025-11-06 00:04:16
