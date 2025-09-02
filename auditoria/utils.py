"""
Utilitários para registro de logs de auditoria
"""
from django.contrib.contenttypes.models import ContentType
from .models import ActivityLog
from .local import get_current_request


def _meta_from_request():
    """
    Extrai IP e User-Agent da requisição atual
    """
    req = get_current_request()
    if not req:
        return None, None
    
    # Tenta obter o IP real (considerando proxies)
    ip = (
        req.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip() or
        req.META.get("HTTP_X_REAL_IP") or
        req.META.get("REMOTE_ADDR")
    ) or None
    
    # User Agent
    ua = req.META.get("HTTP_USER_AGENT", "")
    
    return ip, ua


def log_action(actor, action, instance=None, changes=None, object_repr=None):
    """
    Registra uma ação no log de auditoria
    
    Args:
        actor: Usuário que executou a ação
        action: Tipo da ação ('create', 'update', 'delete', 'login', 'logout')
        instance: Instância do objeto afetado (opcional)
        changes: Dicionário com as mudanças realizadas (opcional)
        object_repr: Representação textual do objeto (opcional)
    """
    ip, ua = _meta_from_request()
    
    # Informações do objeto (se fornecido)
    ct = obj_id = None
    if instance is not None:
        ct = ContentType.objects.get_for_model(instance.__class__)
        obj_id = str(getattr(instance, "pk", None))
        if not object_repr:
            object_repr = str(instance)
    
    # Cria o log
    ActivityLog.objects.create(
        actor=actor if actor and getattr(actor, "is_authenticated", False) else None,
        action=action,
        content_type=ct,
        object_id=obj_id,
        object_repr=object_repr,
        changes=changes or None,
        ip=ip,
        user_agent=ua
    )


def log_login(user):
    """Registra login do usuário"""
    log_action(
        actor=user,
        action="login",
        object_repr=f"Login: {user.username}"
    )


def log_logout(user):
    """Registra logout do usuário"""
    log_action(
        actor=user,
        action="logout",
        object_repr=f"Logout: {getattr(user, 'username', 'anônimo')}"
    )


def log_create(user, instance):
    """Registra criação de objeto"""
    log_action(
        actor=user,
        action="create",
        instance=instance
    )


def log_update(user, instance, changes):
    """Registra atualização de objeto"""
    if changes:  # Só loga se houve mudanças
        log_action(
            actor=user,
            action="update",
            instance=instance,
            changes=changes
        )


def log_delete(user, instance):
    """Registra exclusão de objeto"""
    log_action(
        actor=user,
        action="delete",
        instance=instance
    )