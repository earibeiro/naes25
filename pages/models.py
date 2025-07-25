from django.db import models
from django.contrib.auth.models import User

class State(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome do Estado")
    abbreviation = models.CharField(max_length=2, verbose_name="Sigla", unique=True)
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"
    
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['name']

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome da Cidade")
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="Estado")
    
    def __str__(self):
        return f"{self.name}/{self.state.abbreviation}"
    
    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        ordering = ['name']

class Person(models.Model):
    # Dados pessoais LGPD
    full_name = models.CharField(max_length=150, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, verbose_name="CPF", unique=True)
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(max_length=15, verbose_name="Telefone")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    
    # Endereço
    address = models.CharField(max_length=200, verbose_name="Endereço")
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Cidade")
    
    # Controle LGPD
    consent_date = models.DateTimeField(auto_now_add=True, verbose_name="Data do Consentimento")
    data_processing_purpose = models.TextField(verbose_name="Finalidade do Tratamento")
    
    # RELACIONAMENTO COM USUÁRIO - Quem cadastrou/gerencia estes dados
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Controlador de Dados")
    
    def __str__(self):
        return f"{self.full_name} - {self.cpf}"
    
    class Meta:
        verbose_name = "Pessoa Física"
        verbose_name_plural = "Pessoas Físicas"
        ordering = ['full_name']

class Company(models.Model):
    # Dados empresariais LGPD
    corporate_name = models.CharField(max_length=200, verbose_name="Razão Social")
    trade_name = models.CharField(max_length=200, verbose_name="Nome Fantasia", blank=True)
    cnpj = models.CharField(max_length=18, verbose_name="CNPJ", unique=True)
    email = models.EmailField(verbose_name="E-mail Corporativo")
    phone = models.CharField(max_length=15, verbose_name="Telefone")
    
    # Endereço
    address = models.CharField(max_length=200, verbose_name="Endereço")
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Cidade")
    
    # Dados do responsável LGPD
    data_controller_name = models.CharField(max_length=150, verbose_name="Nome do Encarregado de Dados")
    data_controller_email = models.EmailField(verbose_name="E-mail do Encarregado")
    
    # Controle LGPD
    consent_date = models.DateTimeField(auto_now_add=True, verbose_name="Data do Consentimento")
    data_processing_purpose = models.TextField(verbose_name="Finalidade do Tratamento")
    
    # RELACIONAMENTO COM USUÁRIO - Quem cadastrou/gerencia estes dados
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Controlador de Dados")
    
    def __str__(self):
        return f"{self.corporate_name} - {self.cnpj}"
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['corporate_name']

