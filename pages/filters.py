"""
Filtros usando django-filter para as ListViews
"""
import django_filters as df
from django import forms
from .models import Contract, Company, Person


class ContractFilter(df.FilterSet):
    """
    Filtro para contratos com campos de busca por:
    - Título (icontains)
    - Empresa (icontains no nome da empresa)
    - Pessoa (icontains no nome da pessoa)
    - Tipo de contrato (exact)
    - Status ativo (exact)
    - Data de criação (gte/lte)
    """
    title = df.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        label="Título",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título...'
        })
    )
    
    empresa = df.CharFilter(
        field_name="company__corporate_name",
        lookup_expr="icontains",
        label="Empresa",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por empresa...'
        })
    )
    
    pessoa = df.CharFilter(
        field_name="person__full_name",
        lookup_expr="icontains",
        label="Pessoa",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por pessoa...'
        })
    )
    
    contract_type = df.ChoiceFilter(
        field_name="contract_type",
        lookup_expr="exact",
        label="Tipo de Contrato",
        choices=[
            ('', 'Todos'),
            ('TRABALHO', 'Contrato de Trabalho'),
            ('SERVICO', 'Prestação de Serviços'),
            ('FORNECIMENTO', 'Fornecimento'),
            ('PARCERIA', 'Parceria'),
            ('OUTRO', 'Outro'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    is_active = df.BooleanFilter(
        field_name="is_active",
        lookup_expr="exact",
        label="Status",
        widget=forms.Select(
            choices=[
                ('', 'Todos'),
                ('true', 'Ativo'),
                ('false', 'Inativo'),
            ],
            attrs={'class': 'form-select'}
        )
    )
    
    criado_de = df.DateFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Criado a partir de",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    criado_ate = df.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Criado até",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = Contract
        fields = ["title", "empresa", "pessoa", "contract_type", "is_active", "criado_de", "criado_ate"]


class CompanyFilter(df.FilterSet):
    """
    Filtro para empresas com campos de busca por:
    - Nome/Razão Social (icontains)
    - CNPJ (icontains)
    - Cidade (icontains)
    - Data de criação (gte/lte)
    """
    nome = df.CharFilter(
        field_name="corporate_name",
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
        label="Criada a partir de",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    criada_ate = df.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Criada até",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = Company
        fields = ["nome", "cnpj", "cidade", "criada_de", "criada_ate"]


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
        label="Criada a partir de",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    criada_ate = df.DateFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Criada até",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = Person
        fields = ["nome", "cpf", "cidade", "criada_de", "criada_ate"]