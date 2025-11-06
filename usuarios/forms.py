from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


# Adicionar classes CSS aos campos de formulário
class BaseSignupForm(UserCreationForm):
    """Formulário base para cadastro de usuários"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome de usuário'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar classes Bootstrap aos campos de senha
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })

    def clean_email(self):
        """Validação para evitar emails duplicados"""
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe um usuário com este e-mail.")
        return email


class AdminSignupForm(BaseSignupForm):
    """Cadastro que adiciona ao grupo empresa_admin"""
    
    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            admin_group, _ = Group.objects.get_or_create(name="empresa_admin")
            user.groups.add(admin_group)
        return user


class FuncionarioSignupForm(BaseSignupForm):
    """Cadastro que adiciona ao grupo funcionario"""
    
    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            func_group, _ = Group.objects.get_or_create(name="funcionario")
            user.groups.add(func_group)
        return user


# Manter formulários existentes para compatibilidade
class CadastroPessoaFisicaForm(FuncionarioSignupForm):
    """Alias para pessoa física (funcionário)"""
    pass


class CadastroPessoaJuridicaForm(AdminSignupForm):
    """Alias para pessoa jurídica (admin)"""
    pass


# Formulário customizado para alteração de senha (opcional)
class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulário customizado para alterar senha com classes CSS"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adicionar classes CSS aos campos
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Digite sua {field.label.lower()}'
            })
# Deploy: 2025-11-06 00:04:16
