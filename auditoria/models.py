from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class ActivityLog(models.Model):
    """
    Modelo para registrar todas as ações do sistema (audit trail)
    """
    ACTIONS = [
        ("create", "Criar"),
        ("update", "Atualizar"),
        ("delete", "Excluir"),
        ("login", "Login"),
        ("logout", "Logout"),
    ]
    
    # Quem fez a ação
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="activities",
        verbose_name="Usuário"
    )
    
    # Que ação foi feita
    action = models.CharField(
        max_length=20, 
        choices=ACTIONS,
        verbose_name="Ação"
    )
    
    # Em que objeto (usando GenericForeignKey para qualquer modelo)
    content_type = models.ForeignKey(
        ContentType, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        verbose_name="Tipo de Objeto"
    )
    object_id = models.CharField(
        max_length=64, 
        null=True, 
        blank=True,
        verbose_name="ID do Objeto"
    )
    target = GenericForeignKey("content_type", "object_id")
    
    # Representação textual do objeto
    object_repr = models.CharField(
        max_length=255, 
        blank=True,
        verbose_name="Descrição do Objeto"
    )
    
    # Mudanças realizadas (JSON com campo: [valor_antigo, valor_novo])
    changes = models.JSONField(
        null=True, 
        blank=True,
        verbose_name="Alterações",
        help_text="JSON com as mudanças realizadas"
    )
    
    # Metadados da requisição
    ip = models.GenericIPAddressField(
        null=True, 
        blank=True,
        verbose_name="Endereço IP"
    )
    user_agent = models.TextField(
        blank=True, 
        default="",
        verbose_name="User Agent"
    )
    
    # Controle temporal
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data/Hora"
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Log de Atividade"
        verbose_name_plural = "Logs de Atividades"
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['actor', '-created_at']),
            models.Index(fields=['action', '-created_at']),
            models.Index(fields=['content_type', '-created_at']),
        ]

    def __str__(self):
        who = self.actor.get_username() if self.actor else "anônimo"
        action_display = self.get_action_display()
        target = self.object_repr or f"#{self.object_id}" if self.object_id else "sistema"
        return f"[{self.created_at:%d/%m/%Y %H:%M}] {who} {action_display.lower()} {target}"
    
    def get_changes_display(self):
        """Retorna as mudanças em formato legível"""
        if not self.changes:
            return "Nenhuma alteração registrada"
        
        changes_list = []
        for field, (old_val, new_val) in self.changes.items():
            changes_list.append(f"{field}: '{old_val}' → '{new_val}'")
        
        return "; ".join(changes_list)
    
    @property
    def action_icon(self):
        """Retorna ícone FontAwesome para a ação"""
        icons = {
            'create': 'fas fa-plus-circle text-success',
            'update': 'fas fa-edit text-warning',
            'delete': 'fas fa-trash text-danger',
            'login': 'fas fa-sign-in-alt text-info',
            'logout': 'fas fa-sign-out-alt text-secondary',
        }
        return icons.get(self.action, 'fas fa-question-circle')
    
    @property
    def action_color(self):
        """Retorna cor CSS para a ação"""
        colors = {
            'create': 'success',
            'update': 'warning',
            'delete': 'danger',
            'login': 'info',
            'logout': 'secondary',
        }
        return colors.get(self.action, 'primary')
