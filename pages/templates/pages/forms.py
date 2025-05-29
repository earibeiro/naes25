from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from .models import State, City, Person, Company

class BaseFormMixin:
    """Mixin para configurações básicas dos formulários"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-dark'
        self.helper.label_class = 'text-white'
        self.helper.field_class = 'mb-3'
        
        # Personalizar campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control bg-dark text-white border-secondary',
                'style': 'border-radius: 0.5rem;'
            })
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs['placeholder'] = field.label

class StateForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = State
        fields = ['name', 'abbreviation']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper.layout = Layout(
            HTML('<div class="text-center mb-4">'),
            HTML('<h3 class="text-white mb-3"><i class="fas fa-map me-2"></i>Cadastro de Estado</h3>'),
            HTML('<p class="text-white-50">Preencha os dados do estado</p>'),
            HTML('</div>'),
            
            Row(
                Column('name', css_class='form-group col-md-8 mb-3'),
                Column('abbreviation', css_class='form-group col-md-4 mb-3'),
            ),
            
            Div(
                Submit('submit', 'Cadastrar Estado', 
                       css_class='btn btn-primary btn-lg px-5'),
                css_class='text-center mt-4'
            )
        )

class CityForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'state']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper.layout = Layout(
            HTML('<div class="text-center mb-4">'),
            HTML('<h3 class="text-white mb-3"><i class="fas fa-city me-2"></i>Cadastro de Cidade</h3>'),
            HTML('<p class="text-white-50">Preencha os dados da cidade</p>'),
            HTML('</div>'),
            
            Row(
                Column('name', css_class='form-group col-md-8 mb-3'),
                Column('state', css_class='form-group col-md-4 mb-3'),
            ),
            
            Div(
                Submit('submit', 'Cadastrar Cidade', 
                       css_class='btn btn-primary btn-lg px-5'),
                css_class='text-center mt-4'
            )
        )

class PersonForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'cpf', 'email', 'phone', 'city']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper.layout = Layout(
            HTML('<div class="text-center mb-4">'),
            HTML('<h3 class="text-white mb-3"><i class="fas fa-user me-2"></i>Cadastro de Pessoa Física</h3>'),
            HTML('<p class="text-white-50">Preencha os dados da pessoa física</p>'),
            HTML('</div>'),
            
            Row(
                Column('name', css_class='form-group col-md-8 mb-3'),
                Column('cpf', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('email', css_class='form-group col-md-8 mb-3'),
                Column('phone', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('city', css_class='form-group col-md-12 mb-3'),
            ),
            
            Div(
                Submit('submit', 'Cadastrar Pessoa Física', 
                       css_class='btn btn-primary btn-lg px-5'),
                css_class='text-center mt-4'
            )
        )

class CompanyForm(BaseFormMixin, forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'cnpj', 'email', 'phone', 'city']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper.layout = Layout(
            HTML('<div class="text-center mb-4">'),
            HTML('<h3 class="text-white mb-3"><i class="fas fa-building me-2"></i>Cadastro de Pessoa Jurídica</h3>'),
            HTML('<p class="text-white-50">Preencha os dados da pessoa jurídica</p>'),
            HTML('</div>'),
            
            Row(
                Column('name', css_class='form-group col-md-8 mb-3'),
                Column('cnpj', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('email', css_class='form-group col-md-8 mb-3'),
                Column('phone', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('city', css_class='form-group col-md-12 mb-3'),
            ),
            
            Div(
                Submit('submit', 'Cadastrar Pessoa Jurídica', 
                       css_class='btn btn-primary btn-lg px-5'),
                css_class='text-center mt-4'
            )
        )