from django.contrib.auth.models import Group


def ensure_groups(sender, **kwargs):
    """
    Garante que os grupos necessários existam após as migrações
    """
    for name in ("empresa_admin", "funcionario"):
        group, created = Group.objects.get_or_create(name=name)
        if created:
            print(f"✅ Grupo '{name}' criado com sucesso")
        else:
            print(f"ℹ️ Grupo '{name}' já existe")