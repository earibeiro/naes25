from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    # Importar sinais para criar grupos automaticamente.
    def ready(self):
        import pages.signals

# Deploy: 2025-11-06 00:04:16
