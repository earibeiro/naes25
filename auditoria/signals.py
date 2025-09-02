"""
Signals para capturar automaticamente ações de CRUD nos modelos
"""
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .utils import log_action
from .local import get_current_request

# Lista de modelos que serão monitorados (preenchida no apps.py)
MONITORED_MODELS = []


def diff_instances(old, new, exclude=("id", "pk", "created_at", "updated_at", "usuario")):
    """
    Compara duas instâncias e retorna as diferenças
    
    Args:
        old: Estado anterior do objeto (dict)
        new: Estado atual do objeto (dict)
        exclude: Campos a serem ignorados na comparação
    
    Returns:
        dict: Dicionário com as mudanças no formato {campo: [valor_antigo, valor_novo]}
    """
    changes = {}
    
    for k, v_old in old.items():
        if k in exclude:
            continue
            
        v_new = new.get(k)
        
        # Converte valores para string para comparação
        v_old_str = str(v_old) if v_old is not None else None
        v_new_str = str(v_new) if v_new is not None else None
        
        if v_old_str != v_new_str:
            changes[k] = [v_old_str, v_new_str]
    
    return changes or None


@receiver(pre_save)
def _pre_save_snapshot(sender, instance, **kwargs):
    """
    Captura o estado anterior do objeto antes da atualização
    """
    if sender.__name__ not in MONITORED_MODELS:
        return
    
    # Só captura estado para atualizações (quando já tem PK)
    if not getattr(instance, "pk", None):
        return
    
    try:
        old_instance = sender.objects.get(pk=instance.pk)
        instance.__old_state = model_to_dict(old_instance)
    except sender.DoesNotExist:
        instance.__old_state = None


@receiver(post_save)
def _post_save_log(sender, instance, created, **kwargs):
    """
    Registra criação ou atualização de objetos
    """
    if sender.__name__ not in MONITORED_MODELS:
        return
    
    req = get_current_request()
    user = getattr(req, "user", None) if req else None
    
    if created:
        # Objeto foi criado
        log_action(user, "create", instance=instance)
    else:
        # Objeto foi atualizado - verificar mudanças
        old_state = getattr(instance, "__old_state", None)
        if old_state:
            new_state = model_to_dict(instance)
            changes = diff_instances(old_state, new_state)
            
            if changes:
                log_action(user, "update", instance=instance, changes=changes)


@receiver(post_delete)
def _post_delete_log(sender, instance, **kwargs):
    """
    Registra exclusão de objetos
    """
    if sender.__name__ not in MONITORED_MODELS:
        return
    
    req = get_current_request()
    user = getattr(req, "user", None) if req else None
    
    log_action(user, "delete", instance=instance)


@receiver(user_logged_in)
def _on_login(sender, request, user, **kwargs):
    """
    Registra login do usuário
    """
    log_action(
        actor=user,
        action="login",
        object_repr=f"Login: {user.username}"
    )


@receiver(user_logged_out)
def _on_logout(sender, request, user, **kwargs):
    """
    Registra logout do usuário
    """
    log_action(
        actor=user,
        action="logout",
        object_repr=f"Logout: {getattr(user, 'username', 'anônimo')}"
    )