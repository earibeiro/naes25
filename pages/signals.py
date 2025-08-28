from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """
    Cria grupos padrão após migrações
    """
    # Só executar para o app pages
    if sender.name == 'pages':
        # Grupo empresa_admin - acesso total
        admin_group, created = Group.objects.get_or_create(name='empresa_admin')
        if created:
            print("Grupo 'empresa_admin' criado automaticamente")
        
        # Grupo funcionario - acesso limitado
        user_group, created = Group.objects.get_or_create(name='funcionario')
        if created:
            print("Grupo 'funcionario' criado automaticamente")
        
        print("Grupos padrão criados/atualizados com sucesso!")