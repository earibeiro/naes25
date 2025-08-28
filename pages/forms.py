from django import forms
from django.core.exceptions import ValidationError
from .models import Person, Company, Contract, State, City

class PersonForm(forms.ModelForm):
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
                'placeholder': '123.456.789-00',
                'maxlength': '14'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
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
                'class': 'form-control'
            }),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Finalidade do tratamento dos dados'
            }),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'corporate_name', 'trade_name', 'cnpj', 'phone', 
            'email', 'address', 'city', 'data_processing_purpose'
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
                'placeholder': '12.345.678/0001-90',
                'maxlength': '18'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 3333-4444'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contato@empresa.com'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Endereço completo'
            }),
            'city': forms.Select(attrs={
                'class': 'form-control'
            }),
            'data_processing_purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Finalidade do tratamento dos dados'
            }),
        }

class ContractForm(forms.ModelForm):
    """Form para contratos"""
    
    class Meta:
        model = Contract
        fields = [
            'title', 'description', 'contract_type',
            'start_date', 'end_date', 'value',
            'company', 'person', 'data_processing_purpose',
            'is_active'  # ADICIONAR ESTE CAMPO
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Contrato de Trabalho'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descrição detalhada do contrato...'}),
            'contract_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'person': forms.Select(attrs={'class': 'form-select'}),
            'data_processing_purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})  # WIDGET PARA CHECKBOX
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise ValidationError('Data de início não pode ser posterior à data de fim.')
        
        return cleaned_data

class StateForm(forms.ModelForm):
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
                'maxlength': '2'
            }),
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'state']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da cidade'
            }),
            'state': forms.Select(attrs={
                'class': 'form-control'
            }),
        }