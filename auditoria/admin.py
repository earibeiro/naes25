from django.contrib import admin
from django.utils.html import format_html
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """
    Interface administrativa para visualizar logs de auditoria
    """
    list_display = [
        'created_at', 'actor_display', 'action_display', 
        'target_display', 'ip', 'changes_summary'
    ]
    list_filter = [
        'action', 'created_at', 'content_type',
        ('actor', admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = [
        'actor__username', 'object_repr', 'ip', 'user_agent'
    ]
    readonly_fields = [
        'actor', 'action', 'content_type', 'object_id', 'target',
        'object_repr', 'changes', 'ip', 'user_agent', 'created_at'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    # Não permitir edição/criação/exclusão
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def actor_display(self, obj):
        """Exibe o usuário que fez a ação"""
        if obj.actor:
            return format_html(
                '<i class="fas fa-user"></i> {}',
                obj.actor.get_username()
            )
        return format_html('<i class="fas fa-user-slash text-muted"></i> Anônimo')
    actor_display.short_description = 'Usuário'
    
    def action_display(self, obj):
        """Exibe a ação com ícone"""
        return format_html(
            '<i class="{}"></i> {}',
            obj.action_icon,
            obj.get_action_display()
        )
    action_display.short_description = 'Ação'
    
    def target_display(self, obj):
        """Exibe o objeto alvo da ação"""
        if obj.content_type and obj.object_id:
            return format_html(
                '<strong>{}</strong> #{}',
                obj.content_type.model,
                obj.object_id
            )
        return obj.object_repr or '-'
    target_display.short_description = 'Objeto'
    
    def changes_summary(self, obj):
        """Resumo das mudanças realizadas"""
        if not obj.changes:
            return '-'
        
        num_changes = len(obj.changes)
        if num_changes == 1:
            field = list(obj.changes.keys())[0]
            return format_html('<span class="text-info">{} campo alterado: {}</span>', num_changes, field)
        else:
            return format_html('<span class="text-warning">{} campos alterados</span>', num_changes)
    changes_summary.short_description = 'Alterações'
    
    fieldsets = (
        ('Informações da Ação', {
            'fields': ('created_at', 'actor', 'action')
        }),
        ('Objeto Afetado', {
            'fields': ('content_type', 'object_id', 'object_repr')
        }),
        ('Alterações', {
            'fields': ('changes',),
            'classes': ('collapse',)
        }),
        ('Metadados da Requisição', {
            'fields': ('ip', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
