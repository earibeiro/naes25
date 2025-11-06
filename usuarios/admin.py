from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_usuario', 'documento', 'nome_display', 'ativo', 'data_cadastro')
    list_filter = ('tipo_usuario', 'ativo', 'data_cadastro')
    search_fields = ('cpf', 'cnpj', 'nome_completo', 'razao_social', 'user__username')
    readonly_fields = ('data_cadastro',)
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user', 'tipo_usuario', 'ativo')
        }),
        ('Pessoa Física', {
            'fields': ('cpf', 'nome_completo', 'telefone_pf'),
            'classes': ('collapse',)
        }),
        ('Pessoa Jurídica', {
            'fields': ('cnpj', 'razao_social', 'nome_fantasia', 'telefone_pj'),
            'classes': ('collapse',)
        }),
        ('Informações Gerais', {
            'fields': ('email_contato', 'endereco', 'data_cadastro')
        }),
    )

# Deploy: 2025-11-06 00:04:16
