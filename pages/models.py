from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

User = get_user_model()


class State(models.Model):
    """Modelo para estados (UF)"""
    name = models.CharField(max_length=100, verbose_name="Nome do Estado")
    abbreviation = models.CharField(max_length=2, unique=True, verbose_name="Sigla")
    
    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


class City(models.Model):
    """Modelo para cidades"""
    name = models.CharField(max_length=100, verbose_name="Nome da Cidade")
    state = models.ForeignKey(State, on_delete=models.PROTECT, verbose_name="Estado")
    
    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        ordering = ['name']
        unique_together = ['name', 'state']
    
    def __str__(self):
        return f"{self.name}/{self.state.abbreviation}"


class Person(models.Model):
    """
    Modelo para pessoas físicas
    """
    # Dados pessoais
    full_name = models.CharField(max_length=200, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    
    # ✅ Phone opcional (pode preencher depois)
    phone = models.CharField(
        max_length=20,
        verbose_name="Telefone",
        blank=True,
        default=""
    )
    
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    address = models.CharField(max_length=255, verbose_name="Endereço")
    
    # Localização
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Cidade")
    
    # ✅ LGPD - Opcional inicialmente (pode preencher depois)
    data_processing_purpose = models.TextField(
        verbose_name="Finalidade do Tratamento de Dados",
        help_text="Descreva a finalidade do tratamento dos dados pessoais conforme LGPD",
        blank=True,
        default=""
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
    """
    Modelo para empresas (pessoas jurídicas)
    """
    # Dados básicos obrigatórios
    corporate_name = models.CharField(max_length=200, verbose_name="Razão Social")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    
    # ✅ TODOS OS CAMPOS OPCIONAIS COM blank=True E default
    trade_name = models.CharField(
        max_length=200,
        verbose_name="Nome Fantasia",
        blank=True,
        default=""
    )
    
    phone = models.CharField(
        max_length=15,
        verbose_name="Telefone",
        blank=True,
        default=""
    )
    
    address = models.CharField(
        max_length=200,
        verbose_name="Endereço",
        blank=True,
        default=""
    )
    
    # Encarregado de dados (LGPD) - Opcionais
    data_controller_name = models.CharField(
        max_length=150,
        verbose_name="Nome do Encarregado de Dados",
        blank=True,
        default="",
        help_text="Nome do DPO (Data Protection Officer)"
    )
    
    data_controller_email = models.EmailField(
        verbose_name="E-mail do Encarregado",
        blank=True,
        default="",
        help_text="E-mail de contato do DPO"
    )
    
    # LGPD - consent_date automático
    consent_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Data do Consentimento",
        help_text="Data em que o consentimento LGPD foi registrado"
    )
    
    # Texto do consentimento opcional
    consent_text = models.TextField(
        verbose_name="Texto do Consentimento LGPD",
        blank=True,
        default="",
        help_text="Termo de consentimento para tratamento de dados"
    )
    
    # Localização
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        verbose_name="Cidade",
        null=True,  # ✅ Permitir NULL durante migração
        blank=True
    )
    
    # Contador de contratos (automático)
    total_contracts = models.IntegerField(
        default=0,
        verbose_name="Total de Contratos",
        help_text="Número total de contratos ativos vinculados a esta empresa"
    )
    
    # Relacionamento com usuário (owner)
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
    # Tipos de contrato
    CONTRACT_TYPES = [
        ('TRABALHO', 'Contrato de Trabalho'),
        ('SERVICO', 'Prestação de Serviços'),
        ('FORNECIMENTO', 'Fornecimento'),
        ('PARCERIA', 'Parceria'),
        ('OUTRO', 'Outro'),
    ]
    
    # Dados do contrato (obrigatórios)
    title = models.CharField(max_length=200, verbose_name="Título do Contrato")
    
    # ✅ Campos opcionais
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Descrição",
        help_text="Descrição detalhada do contrato"
    )
    
    contract_type = models.CharField(
        max_length=20,
        choices=CONTRACT_TYPES,
        default='SERVICO',
        verbose_name="Tipo de Contrato"
    )
    
    # Datas opcionais
    start_date = models.DateField(
        verbose_name="Data de Início",
        blank=True,
        null=True
    )
    
    end_date = models.DateField(
        verbose_name="Data de Fim",
        blank=True,
        null=True,
        help_text="Deixe em branco para contratos por prazo indeterminado"
    )
    
    # Valor opcional
    value = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        verbose_name="Valor do Contrato",
        blank=True,
        null=True,
        help_text="Valor total do contrato em reais"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name="Contrato Ativo",
        help_text="Indica se o contrato está ativo no sistema"
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
    
    # ✅ LGPD opcional
    data_processing_purpose = models.TextField(
        verbose_name="Finalidade do Tratamento de Dados no Contrato",
        help_text="Descreva como os dados serão tratados neste contrato (LGPD)",
        blank=True,
        default=""
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
        indexes = [
            models.Index(fields=['company', 'is_active']),
            models.Index(fields=['person', 'is_active']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.company} - {self.person})"
    
    def clean(self):
        """Validações customizadas"""
        from django.core.exceptions import ValidationError
        from django.utils import timezone as tz
        
        if self.end_date and self.start_date:
            if self.end_date <= self.start_date:
                raise ValidationError("A data de fim deve ser posterior à data de início.")


class ContractMovement(models.Model):
    """
    Modelo para rastrear movimentações de contratos
    (complementa o sistema de auditoria ActivityLog)
    """
    MOVEMENT_TYPES = [
        ('created', 'Criado'),
        ('updated', 'Atualizado'),
        ('activated', 'Ativado'),
        ('deactivated', 'Desativado'),
        ('deleted', 'Excluído'),
    ]
    
    # Relacionamento com contrato
    contract = models.ForeignKey(
        Contract,
        on_delete=models.CASCADE,
        related_name="movements",
        verbose_name="Contrato"
    )
    
    # Tipo de movimento
    movement_type = models.CharField(
        max_length=30,
        choices=MOVEMENT_TYPES,
        verbose_name="Tipo de Movimento"
    )
    
    # Descrição do movimento (opcional)
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Descrição",
        help_text="Detalhes sobre a movimentação"
    )
    
    # Usuário que executou a ação
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contract_movements",
        verbose_name="Executado por"
    )
    
    # Dados contextuais (JSON) - opcional
    metadata = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Metadados",
        help_text="Informações adicionais sobre a movimentação"
    )
    
    # Controle temporal
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Movimentação"
    )
    
    class Meta:
        verbose_name = "Movimentação de Contrato"
        verbose_name_plural = "Movimentações de Contratos"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['contract', '-created_at']),
            models.Index(fields=['movement_type', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.contract.title} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"
    
    @property
    def movement_icon(self):
        """Retorna ícone FontAwesome para o tipo de movimento"""
        icons = {
            'created': 'fas fa-plus-circle text-success',
            'updated': 'fas fa-edit text-warning',
            'activated': 'fas fa-check-circle text-success',
            'deactivated': 'fas fa-times-circle text-secondary',
            'deleted': 'fas fa-trash text-danger',
        }
        return icons.get(self.movement_type, 'fas fa-question-circle')


# Deploy: 2025-11-06 00:04:16
