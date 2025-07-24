from django import forms
from .models import Person, Company, State, City

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['name', 'abbreviation']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'abbreviation': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '2'}),
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'state']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
        }

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'full_name', 'cpf', 'email', 'phone', 'birth_date', 
            'address', 'city', 'data_processing_purpose'
        ]
        # REMOVIDO 'usuario' - será preenchido automaticamente
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'data_processing_purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'corporate_name', 'trade_name', 'cnpj', 'email', 'phone',
            'address', 'city', 'data_controller_name', 'data_controller_email',
            'data_processing_purpose'
        ]
        # REMOVIDO 'usuario' - será preenchido automaticamente
        
        widgets = {
            'corporate_name': forms.TextInput(attrs={'class': 'form-control'}),
            'trade_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0000-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00) 00000-0000'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'data_controller_name': forms.TextInput(attrs={'class': 'form-control'}),
            'data_controller_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'data_processing_purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }