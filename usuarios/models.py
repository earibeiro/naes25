from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.conf import settings

class UserProfile(models.Model):
    """
    Perfil estendido do usuário para armazenar informações específicas
    """
    TIPO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    # Tipo de usuário
    tipo_usuario = models.CharField(
        max_length=2, 
        choices=TIPO_CHOICES,
        verbose_name="Tipo de Usuário"
    )
    
    # Para Pessoa Física
    cpf = models.CharField(
        max_length=14, 
        verbose_name="CPF",
        blank=True, 
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message="CPF deve estar no formato: 123.456.789-00"
            )
        ]
    )
    nome_completo = models.CharField(
        max_length=200, 
        verbose_name="Nome Completo",
        blank=True
    )
    telefone_pf = models.CharField(
        max_length=20, 
        verbose_name="Telefone",
        blank=True
    )
    
    # Para Pessoa Jurídica
    cnpj = models.CharField(
        max_length=18, 
        verbose_name="CNPJ",
        blank=True, 
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message="CNPJ deve estar no formato: 12.345.678/0001-90"
            )
        ]
    )
    razao_social = models.CharField(
        max_length=200, 
        verbose_name="Razão Social",
        blank=True
    )
    nome_fantasia = models.CharField(
        max_length=200, 
        verbose_name="Nome Fantasia",
        blank=True
    )
    telefone_pj = models.CharField(
        max_length=20, 
        verbose_name="Telefone",
        blank=True
    )
    
    # Campos comuns
    email_contato = models.EmailField(
        verbose_name="Email de Contato",
        blank=True
    )
    endereco = models.CharField(
        max_length=255, 
        verbose_name="Endereço",
        blank=True
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"
    
    def __str__(self):
        if self.tipo_usuario == 'PF':
            return f"{self.nome_completo} - CPF: {self.cpf}"
        else:
            return f"{self.razao_social} - CNPJ: {self.cnpj}"
    
    @property
    def documento(self):
        """Retorna CPF ou CNPJ dependendo do tipo"""
        return self.cpf if self.tipo_usuario == 'PF' else self.cnpj
    
    @property
    def nome_display(self):
        """Retorna nome ou razão social dependendo do tipo"""
        return self.nome_completo if self.tipo_usuario == 'PF' else self.razao_social
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.tipo_usuario == 'PF':
            if not self.cpf:
                raise ValidationError("CPF é obrigatório para Pessoa Física")
            if not self.nome_completo:
                raise ValidationError("Nome completo é obrigatório para Pessoa Física")
        elif self.tipo_usuario == 'PJ':
            if not self.cnpj:
                raise ValidationError("CNPJ é obrigatório para Pessoa Jurídica")
            if not self.razao_social:
                raise ValidationError("Razão social é obrigatória para Pessoa Jurídica")
# Deploy: 2025-11-06 00:04:16
