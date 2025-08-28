from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class State(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    abbreviation = models.CharField(max_length=2, verbose_name="Sigla")
    
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="Estado")
    
    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
    
    def __str__(self):
        return f"{self.name} - {self.state.abbreviation}"

class Person(models.Model):
    # Dados pessoais LGPD
    full_name = models.CharField(max_length=150, verbose_name="Nome Completo")
    cpf = models.CharField(
        max_length=14, 
        verbose_name="CPF", 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF deve estar no formato 000.000.000-00'
            )
        ]
    )
    phone = models.CharField(max_length=15, verbose_name="Telefone")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    
    # Endereço
    address = models.CharField(max_length=200, verbose_name="Endereço")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Cidade")
    
    # LGPD
    data_processing_purpose = models.TextField(verbose_name="Finalidade do Tratamento")
    consent_date = models.DateTimeField(auto_now_add=True, verbose_name="Data do Consentimento")
    
    # ESCOPO POR OWNER - MUDANÇA DE OneToOneField PARA ForeignKey
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="persons",
        verbose_name="Usuário Responsável"
    )
    
    class Meta:
        verbose_name = "Pessoa Física"
        verbose_name_plural = "Pessoas Físicas"
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.full_name} - CPF: {self.cpf}"

class Company(models.Model):
    # Dados empresariais LGPD
    corporate_name = models.CharField(max_length=150, verbose_name="Razão Social")
    trade_name = models.CharField(max_length=150, verbose_name="Nome Fantasia")
    cnpj = models.CharField(
        max_length=18, 
        verbose_name="CNPJ", 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message='CNPJ deve estar no formato 00.000.000/0000-00'
            )
        ]
    )
    phone = models.CharField(max_length=15, verbose_name="Telefone")
    
    # Endereço
    address = models.CharField(max_length=200, verbose_name="Endereço")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Cidade")
    
    # Encarregado de dados LGPD
    data_controller_name = models.CharField(max_length=150, verbose_name="Nome do Encarregado")
    data_controller_email = models.EmailField(verbose_name="E-mail do Encarregado")
    
    # LGPD
    data_processing_purpose = models.TextField(verbose_name="Finalidade do Tratamento")
    consent_date = models.DateTimeField(auto_now_add=True, verbose_name="Data do Consentimento")
    
    # ESCOPO POR OWNER - MUDANÇA DE OneToOneField PARA ForeignKey
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="companies", 
        verbose_name="Usuário Responsável"
    )
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.trade_name} - CNPJ: {self.cnpj}"

