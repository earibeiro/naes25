from django import forms
from django.contrib.auth import get_user_model
from .models import Person, Company, Contract, State, City

User = get_user_model()


class PersonForm(forms.ModelForm):
    """Formulário para Person com suporte ao parâmetro user"""
    
    class Meta:
        model = Person
        fields = [
            'full_name', 'cpf', 'phone', 'birth_date',
            'address', 'city', 'data_processing_purpose'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo da pessoa'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'data-mask': '000.000.000-00'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000',
                'data-mask': '(00) 00000-0000'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Finalidade do tratamento dos dados...'
            }),
        }
        labels = {
            'full_name': 'Nome Completo',
            'cpf': 'CPF',
            'phone': 'Telefone',
            'birth_date': 'Data de Nascimento',
            'address': 'Endereço',
            'city': 'Cidade',
            'data_processing_purpose': 'Finalidade do Tratamento (LGPD)',
        }
    
    def __init__(self, *args, **kwargs):
        # Remove o argumento 'user' se presente para evitar erro
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class CompanyForm(forms.ModelForm):
    """Formulário para Company com suporte ao parâmetro user"""
    
    class Meta:
        model = Company
        # ✅ CORRIGIDO: Usar apenas campos que existem em Company
        fields = [
            'corporate_name', 'trade_name', 'cnpj', 'phone',
            'address', 'city', 
            'data_controller_name', 'data_controller_email',
            'consent_text'
        ]
        widgets = {
            'corporate_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razão social da empresa'
            }),
            'trade_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome fantasia (opcional)'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'XX.XXX.XXX/XXXX-XX',
                'data-mask': 'cnpj'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(XX) XXXXX-XXXX',
                'data-mask': 'telefone'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo da empresa'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_controller_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do Encarregado de Dados (DPO)'
            }),
            'data_controller_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'dpo@empresa.com'
            }),
            'consent_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Texto do consentimento LGPD...'
            }),
        }
        labels = {
            'corporate_name': 'Razão Social',
            'trade_name': 'Nome Fantasia',
            'cnpj': 'CNPJ',
            'phone': 'Telefone',
            'address': 'Endereço',
            'city': 'Cidade',
            'data_controller_name': 'Encarregado de Dados (DPO)',
            'data_controller_email': 'E-mail do Encarregado',
            'consent_text': 'Texto do Consentimento LGPD',
        }
    
    def __init__(self, *args, **kwargs):
        # Remove o argumento 'user' se presente para evitar erro
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class ContractForm(forms.ModelForm):
    """Formulário para Contract com suporte ao parâmetro user"""
    
    class Meta:
        model = Contract
        fields = [
            'title', 'description', 'contract_type', 'person', 'company', 
            'data_processing_purpose', 'start_date', 'end_date', 'value', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Contrato de Prestação de Serviços'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descreva os detalhes do contrato...'
            }),
            'contract_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'person': forms.Select(attrs={
                'class': 'form-select',
                'data-placeholder': 'Selecione a pessoa física...'
            }),
            'company': forms.Select(attrs={
                'class': 'form-select',
                'data-placeholder': 'Selecione a empresa...'
            }),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a finalidade do tratamento dos dados neste contrato...'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'title': 'Título do Contrato',
            'description': 'Descrição',
            'contract_type': 'Tipo de Contrato',
            'person': 'Pessoa Física',
            'company': 'Empresa',
            'data_processing_purpose': 'Finalidade do Tratamento de Dados (LGPD)',
            'start_date': 'Data de Início',
            'end_date': 'Data de Fim',
            'value': 'Valor do Contrato (R$)',
            'is_active': 'Contrato Ativo',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['person'].queryset = Person.objects.filter(usuario=user)
            self.fields['company'].queryset = Company.objects.filter(usuario=user)
            
            self.fields['person'].empty_label = "Selecione a pessoa física..."
            self.fields['company'].empty_label = "Selecione a empresa..."


class StateForm(forms.ModelForm):
    """Formulário para State (apenas admin)"""
    
    class Meta:
        model = State
        fields = ['name', 'abbreviation']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do estado'
            }),
            'abbreviation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UF',
                'maxlength': '2'
            }),
        }
        labels = {
            'name': 'Nome do Estado',
            'abbreviation': 'Sigla (UF)',
        }
    
    def __init__(self, *args, **kwargs):
        # Remove o argumento 'user' se presente
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


class CityForm(forms.ModelForm):
    """Formulário para City (apenas admin)"""
    
    class Meta:
        model = City
        fields = ['name', 'state']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da cidade'
            }),
            'state': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'name': 'Nome da Cidade',
            'state': 'Estado',
        }
    
    def __init__(self, *args, **kwargs):
        # Remove o argumento 'user' se presente
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
# Deploy: 2025-11-06 00:04:16
