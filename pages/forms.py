from django import forms
from django.contrib.auth import get_user_model
from .models import Person, Company, Contract, State, City

User = get_user_model()


class PersonForm(forms.ModelForm):
    """Formulário para pessoas"""
    
    class Meta:
        model = Person
        fields = [
            'full_name', 'cpf', 'phone', 'birth_date', 
            'address', 'city', 'data_processing_purpose'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo'
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo'
            }),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a finalidade do tratamento dos dados pessoais...'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar cidades por usuário se necessário
        if self.user:
            # Admin vê todas as cidades, usuário comum apenas as suas
            if self.user.is_superuser or self.user.groups.filter(name='empresa_admin').exists():
                self.fields['city'].queryset = City.objects.all()
            else:
                # Pode filtrar por cidades do usuário ou deixar todas
                self.fields['city'].queryset = City.objects.all()


class CompanyForm(forms.ModelForm):
    """Formulário para empresas"""
    
    class Meta:
        model = Company
        fields = [
            'corporate_name', 'trade_name', 'cnpj', 'email', 
            'phone', 'address', 'city', 'data_processing_purpose'
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
                'placeholder': '00.000.000/0000-00'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@empresa.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 0000-0000'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço da empresa'
            }),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva a finalidade do tratamento dos dados da empresa...'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar cidades se necessário
        if self.user:
            self.fields['city'].queryset = City.objects.all()


class ContractForm(forms.ModelForm):
    """Formulário para contratos"""
    
    class Meta:
        model = Contract
        fields = [
            'title', 'description', 'contract_type', 'start_date', 
            'end_date', 'value', 'company', 'person', 'is_active',
            'data_processing_purpose'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do contrato'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição detalhada do contrato...'
            }),
            'contract_type': forms.Select(attrs={'class': 'form-select'}),
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
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'person': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva como os dados serão tratados neste contrato...'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar empresas e pessoas pelo usuário
        if self.user:
            if self.user.is_superuser or self.user.groups.filter(name='empresa_admin').exists():
                # Admin vê todas
                self.fields['company'].queryset = Company.objects.all()
                self.fields['person'].queryset = Person.objects.all()
            else:
                # Usuário comum vê apenas suas
                self.fields['company'].queryset = Company.objects.filter(usuario=self.user)
                self.fields['person'].queryset = Person.objects.filter(usuario=self.user)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and end_date <= start_date:
            raise forms.ValidationError("A data de fim deve ser posterior à data de início.")
        
        return cleaned_data


class StateForm(forms.ModelForm):
    """Formulário para estados (apenas admin)"""
    
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
                'placeholder': 'UF'
            }),
        }


class CityForm(forms.ModelForm):
    """Formulário para cidades (apenas admin)"""
    
    class Meta:
        model = City
        fields = ['name', 'state']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da cidade'
            }),
            'state': forms.Select(attrs={'class': 'form-select'}),
        }