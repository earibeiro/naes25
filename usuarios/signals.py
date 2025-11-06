from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def ensure_groups(sender, **kwargs):
    """
    Garante que os grupos necessários existam após as migrações
    """
    required_groups = [
        {
            'name': 'empresa_admin',
            'description': 'Administradores da empresa - acesso total ao sistema'
        },
        {
            'name': 'funcionario', 
            'description': 'Funcionários - acesso limitado aos próprios dados'
        }
    ]
    
    for group_data in required_groups:
        group, created = Group.objects.get_or_create(
            name=group_data['name']
        )
        
        if created:
            print(f"✅ Grupo '{group_data['name']}' criado com sucesso")
            print(f"   📝 {group_data['description']}")
        else:
            print(f"ℹ️ Grupo '{group_data['name']}' já existe")


def assign_user_to_group(user, group_name):
    """
    Função helper para atribuir usuário a um grupo
    """
    try:
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        print(f"✅ Usuário '{user.username}' adicionado ao grupo '{group_name}'")
        return True
    except Group.DoesNotExist:
        print(f"❌ Grupo '{group_name}' não encontrado")
        return False


def remove_user_from_group(user, group_name):
    """
    Função helper para remover usuário de um grupo
    """
    try:
        group = Group.objects.get(name=group_name)
        user.groups.remove(group)
        print(f"✅ Usuário '{user.username}' removido do grupo '{group_name}'")
        return True
    except Group.DoesNotExist:
        print(f"❌ Grupo '{group_name}' não encontrado")
        return False


def get_user_groups(user):
    """
    Função helper para listar grupos do usuário
    """
    return [group.name for group in user.groups.all()]


def is_user_in_group(user, group_name):
    """
    Função helper para verificar se usuário está em grupo
    """
    return user.groups.filter(name=group_name).exists()


def is_admin_user(user):
    """
    Função helper para verificar se é admin
    """
    return user.is_superuser or user.groups.filter(name='empresa_admin').exists()


def is_funcionario_user(user):
    """
    Função helper para verificar se é funcionário
    """
    return user.groups.filter(name='funcionario').exists()


def is_staff_user(user):
    """
    Função helper para verificar se é staff (funcionário OU admin)
    """
    return (
        user.is_superuser or 
        user.groups.filter(name__in=['empresa_admin', 'funcionario']).exists()
    )
# Deploy: 2025-11-06 00:04:16
