from django.apps import AppConfig


class AuditoriaConfig(AppConfig):
    """
    Configuração do app de auditoria
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auditoria'
    verbose_name = 'Auditoria'

    def ready(self):
        """
        Registra os signals e configura os modelos monitorados
        """
        from . import signals
        from django.apps import apps
        
        # Modelos que serão monitorados pela auditoria
        target_models = [
            'pages.Person',      # Pessoas
            'pages.Company',     # Empresas  
            'pages.Contract',    # Contratos
            'pages.State',       # Estados (apenas admin)
            'pages.City',        # Cidades (apenas admin)
        ]
        
        # Registra os modelos que existem
        monitored = []
        for model_label in target_models:
            try:
                model = apps.get_model(model_label)
                monitored.append(model.__name__)
            except Exception as e:
                print(f"⚠️ Modelo {model_label} não encontrado para auditoria: {e}")
        
        # Atualiza a lista de modelos monitorados
        signals.MONITORED_MODELS[:] = monitored
        
        if monitored:
            print(f"✅ Auditoria ativada para modelos: {', '.join(monitored)}")
