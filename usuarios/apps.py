from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    verbose_name = 'Usuários'

    def ready(self):
        from django.db.models.signals import post_migrate
        from .signals import ensure_groups
        post_migrate.connect(ensure_groups, sender=self)

# Deploy: 2025-11-06 00:04:16
