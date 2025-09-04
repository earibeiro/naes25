from django import forms
from django.contrib.auth import get_user_model
from .models import Person, Company, Contract, State, City

User = get_user_model()


class PersonForm(forms.ModelForm):
    """Formulário para Person com suporte ao parâmetro user"""
    
    class Meta:
        model = Person
        fields = [
            'full_name', 'birth_date', 'cpf', 'phone', 
            'address', 'city', 'data_processing_purpose'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo da pessoa'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'XXX.XXX.XXX-XX',
                'data-mask': '000.000.000-00'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(XX) XXXXX-XXXX',
                'data-mask': '(00) 00000-0000'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, número, bairro'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a finalidade do tratamento dos dados pessoais...'
            }),
        }
        labels = {
            'full_name': 'Nome Completo',
            'birth_date': 'Data de Nascimento',
            'cpf': 'CPF',
            'phone': 'Telefone',
            'address': 'Endereço',
            'city': 'Cidade',
            'data_processing_purpose': 'Finalidade do Tratamento (LGPD)',
        }
    
    def __init__(self, *args, **kwargs):
        # Remove o argumento 'user' se presente para evitar erro
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar cidades por usuário se necessário
        if self.user and not self.user.is_superuser:
            # Lógica de filtro por usuário pode ser implementada aqui
            pass


class CompanyForm(forms.ModelForm):
    """Formulário para Company com suporte ao parâmetro user"""
    
    class Meta:
        model = Company
        fields = [
            'corporate_name', 'trade_name', 'cnpj', 'phone', 'email',
            'address', 'city', 'data_processing_purpose'
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
                'data-mask': '00.000.000/0000-00'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(XX) XXXXX-XXXX',
                'data-mask': '(00) 00000-0000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contato@empresa.com'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo da empresa'
            }),
            'city': forms.Select(attrs={
                'class': 'form-select'
            }),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Finalidade do tratamento dos dados da empresa...'
            }),
        }
        labels = {
            'corporate_name': 'Razão Social',
            'trade_name': 'Nome Fantasia',
            'cnpj': 'CNPJ',
            'phone': 'Telefone',
            'email': 'E-mail',
            'address': 'Endereço',
            'city': 'Cidade',
            'data_processing_purpose': 'Finalidade do Tratamento (LGPD)',
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
            'data_processing_purpose', 'start_date', 'end_date'
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
                'data-placeholder': 'Selecione a empresa (opcional)...'
            }),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ex: Tratamento de dados para execução do contrato de serviços...'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['person'].queryset = Person.objects.filter(usuario=user)
            self.fields['company'].queryset = Company.objects.filter(usuario=user)
            
            self.fields['person'].empty_label = "Selecione a pessoa física..."
            self.fields['company'].empty_label = "Selecione a empresa (opcional)..."
        

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
                'placeholder': 'SP',
                'maxlength': 2
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