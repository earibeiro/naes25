from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import RegexValidator
from decimal import Decimal

User = get_user_model()

class State(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Estado")
    abbreviation = models.CharField(max_length=2, verbose_name="Sigla", unique=True)
    
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Cidade")
    state = models.ForeignKey(
        State, 
        on_delete=models.CASCADE, 
        related_name='cities',
        verbose_name="Estado"
    )
    
    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        ordering = ['name']
        unique_together = ['name', 'state']
    
    def __str__(self):
        return f"{self.name} - {self.state.abbreviation}"

class Person(models.Model):
    # Dados pessoais
    full_name = models.CharField(max_length=200, verbose_name="Nome Completo")
    cpf = models.CharField(
        max_length=14, 
        verbose_name="CPF", 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message="CPF deve estar no formato: 123.456.789-00"
            )
        ]
    )
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    
    # Endereço
    address = models.CharField(max_length=255, verbose_name="Endereço")
    city = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        verbose_name="Cidade"
    )
    
    # LGPD
    data_processing_purpose = models.TextField(
        verbose_name="Finalidade do Tratamento de Dados",
        help_text="Descreva a finalidade do tratamento dos dados pessoais conforme LGPD"
    )
    
    # Relacionamento
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="person",
        verbose_name="Usuário Responsável"
    )
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Pessoa Física"
        verbose_name_plural = "Pessoas Físicas"
        ordering = ['full_name']
    
    def __str__(self):
        return self.full_name

class Company(models.Model):
    # Dados da empresa
    corporate_name = models.CharField(max_length=200, verbose_name="Razão Social")
    trade_name = models.CharField(
        max_length=200, 
        verbose_name="Nome Fantasia", 
        blank=True, 
        null=True
    )
    cnpj = models.CharField(
        max_length=18, 
        verbose_name="CNPJ",
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message="CNPJ deve estar no formato: 12.345.678/0001-90"
            )
        ]
    )
    phone = models.CharField(max_length=20, verbose_name="Telefone", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    
    # Endereço
    address = models.CharField(max_length=255, verbose_name="Endereço")
    city = models.ForeignKey(
        City, 
        on_delete=models.CASCADE, 
        verbose_name="Cidade"
    )
    
    # LGPD
    data_processing_purpose = models.TextField(
        verbose_name="Finalidade do Tratamento de Dados",
        help_text="Descreva a finalidade do tratamento dos dados da empresa conforme LGPD"
    )
    
    # Relacionamento
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="companies",
        verbose_name="Usuário Responsável"
    )
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['corporate_name']
    
    def __str__(self):
        return self.trade_name if self.trade_name else self.corporate_name

class Contract(models.Model):
    """
    Modelo para contratos entre empresas e pessoas
    """
    
    # Choices para tipo de contrato
    CONTRACT_TYPES = [
        ('servico', 'Prestação de Serviços'),
        ('trabalho', 'Contrato de Trabalho'),
        ('fornecimento', 'Fornecimento'),
        ('consultoria', 'Consultoria'),
        ('manutencao', 'Manutenção'),
        ('licenca', 'Licença de Software'),
        ('outro', 'Outro'),
    ]
    
    # Dados básicos do contrato
    title = models.CharField(max_length=200, verbose_name="Título do Contrato")
    description = models.TextField(verbose_name="Descrição do Contrato")
    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPES,
        verbose_name="Tipo de Contrato",
        default='servico'
    )
    
    # Datas
    start_date = models.DateField(verbose_name="Data de Início")
    end_date = models.DateField(
        verbose_name="Data de Fim", 
        blank=True, 
        null=True,
        help_text="Deixe em branco para contratos por prazo indeterminado"
    )
    
    # Valor
    value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Valor do Contrato",
        blank=True,
        null=True,
        help_text="Valor total do contrato em reais"
    )
    
    # Relacionamentos
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="contracts",
        verbose_name="Empresa"
    )
    
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="contracts",
        verbose_name="Pessoa"
    )
    
    # LGPD
    data_processing_purpose = models.TextField(
        verbose_name="Finalidade do Tratamento de Dados no Contrato",
        help_text="Descreva como os dados serão tratados neste contrato (LGPD)"
    )
    
    # Relacionamento com usuário (owner)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="contracts",
        verbose_name="Usuário Responsável"
    )
    
    # Controle
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.company} x {self.person}"
    
    @property
    def is_active(self):
        """Verifica se o contrato está ativo"""
        from django.utils import timezone
        today = timezone.now().date()
        
        if self.end_date:
            return self.start_date <= today <= self.end_date
        else:
            return self.start_date <= today
    
    @property
    def duration_days(self):
        """Calcula a duração em dias"""
        if self.end_date:
            return (self.end_date - self.start_date).days
        return None
    
    def clean(self):
        """Validações customizadas"""
        from django.core.exceptions import ValidationError
        
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError('Data de início não pode ser posterior à data de fim.')

