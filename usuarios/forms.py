from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError

class CadastroPessoaFisicaForm(UserCreationForm):
    """Form para cadastro de Pessoa Física"""
    
    # Campos do User
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu.email@exemplo.com'
        })
    )
    
    # Campos do Profile
    cpf = forms.CharField(
        max_length=14,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123.456.789-00',
            'data-mask': '000.000.000-00'
        }),
        label="CPF"
    )
    
    nome_completo = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome completo'
        }),
        label="Nome Completo"
    )
    
    telefone_pf = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999',
            'data-mask': '(00) 00000-0000'
        }),
        label="Telefone"
    )
    
    endereco = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu endereço completo'
        }),
        label="Endereço"
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escolha um nome de usuário'
            }),
        }
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            # Verificar se CPF já existe
            if UserProfile.objects.filter(cpf=cpf).exists():
                raise ValidationError("Este CPF já está cadastrado no sistema.")
        return cpf
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar se email já existe
            if User.objects.filter(email=email).exists():
                raise ValidationError("Este email já está cadastrado no sistema.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nome_completo'].split()[0]
        user.last_name = ' '.join(self.cleaned_data['nome_completo'].split()[1:])
        
        if commit:
            user.save()
            # Criar perfil
            UserProfile.objects.create(
                user=user,
                tipo_usuario='PF',
                cpf=self.cleaned_data['cpf'],
                nome_completo=self.cleaned_data['nome_completo'],
                telefone_pf=self.cleaned_data.get('telefone_pf', ''),
                endereco=self.cleaned_data.get('endereco', ''),
                email_contato=self.cleaned_data['email']
            )
        return user

class CadastroPessoaJuridicaForm(UserCreationForm):
    """Form para cadastro de Pessoa Jurídica"""
    
    # Campos do User
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'contato@empresa.com'
        })
    )
    
    # Campos do Profile
    cnpj = forms.CharField(
        max_length=18,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678/0001-90',
            'data-mask': '00.000.000/0000-00'
        }),
        label="CNPJ"
    )
    
    razao_social = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Razão Social da Empresa'
        }),
        label="Razão Social"
    )
    
    nome_fantasia = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome Fantasia (opcional)'
        }),
        label="Nome Fantasia"
    )
    
    telefone_pj = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 3333-4444',
            'data-mask': '(00) 0000-0000'
        }),
        label="Telefone"
    )
    
    endereco = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Endereço da empresa'
        }),
        label="Endereço"
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escolha um nome de usuário'
            }),
        }
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj:
            # Verificar se CNPJ já existe
            if UserProfile.objects.filter(cnpj=cnpj).exists():
                raise ValidationError("Este CNPJ já está cadastrado no sistema.")
        return cnpj
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            # Verificar se email já existe
            if User.objects.filter(email=email).exists():
                raise ValidationError("Este email já está cadastrado no sistema.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['razao_social'][:30]  # Limitado a 30 chars
        
        if commit:
            user.save()
            # Criar perfil
            UserProfile.objects.create(
                user=user,
                tipo_usuario='PJ',
                cnpj=self.cleaned_data['cnpj'],
                razao_social=self.cleaned_data['razao_social'],
                nome_fantasia=self.cleaned_data.get('nome_fantasia', ''),
                telefone_pj=self.cleaned_data.get('telefone_pj', ''),
                endereco=self.cleaned_data.get('endereco', ''),
                email_contato=self.cleaned_data['email']
            )
        return user