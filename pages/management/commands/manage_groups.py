from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from usuarios.signals import assign_user_to_group, remove_user_from_group, get_user_groups


class Command(BaseCommand):
    """
    Comando para gerenciar grupos de usuários
    
    Uso:
    python manage.py manage_groups --list-users
    python manage.py manage_groups --add-user admin funcionario
    python manage.py manage_groups --remove-user user1 empresa_admin
    python manage.py manage_groups --list-groups user1
    """
    
    help = 'Gerencia grupos de usuários no sistema'
    
    def add_arguments(self, parser):
        parser.add_argument('--list-users', action='store_true', help='Lista todos os usuários e seus grupos')
        parser.add_argument('--list-groups', help='Lista grupos de um usuário específico')
        parser.add_argument('--add-user', nargs=2, metavar=('USERNAME', 'GROUP'), help='Adiciona usuário a um grupo')
        parser.add_argument('--remove-user', nargs=2, metavar=('USERNAME', 'GROUP'), help='Remove usuário de um grupo')
        parser.add_argument('--create-groups', action='store_true', help='Cria grupos necessários')
    
    def handle(self, *args, **options):
        
        if options['list_users']:
            self.list_all_users()
        
        elif options['list_groups']:
            self.list_user_groups(options['list_groups'])
        
        elif options['add_user']:
            username, group_name = options['add_user']
            self.add_user_to_group(username, group_name)
        
        elif options['remove_user']:
            username, group_name = options['remove_user']
            self.remove_user_from_group(username, group_name)
        
        elif options['create_groups']:
            self.create_required_groups()
        
        else:
            self.stdout.write(self.style.WARNING('Use --help para ver as opções disponíveis'))
    
    def list_all_users(self):
        """Lista todos os usuários e seus grupos"""
        self.stdout.write(self.style.SUCCESS('📋 USUÁRIOS E GRUPOS'))
        self.stdout.write('=' * 60)
        
        for user in User.objects.all().order_by('username'):
            groups = get_user_groups(user)
            status = "🔴 Superuser" if user.is_superuser else "👤 Regular"
            groups_str = ', '.join(groups) if groups else 'Nenhum grupo'
            
            self.stdout.write(f"{status} {user.username} ({user.email})")
            self.stdout.write(f"   🏷️ Grupos: {groups_str}")
            self.stdout.write('')
    
    def list_user_groups(self, username):
        """Lista grupos de um usuário específico"""
        try:
            user = User.objects.get(username=username)
            groups = get_user_groups(user)
            
            self.stdout.write(self.style.SUCCESS(f'👤 Usuário: {username}'))
            self.stdout.write(f'📧 Email: {user.email}')
            self.stdout.write(f'🔐 Superuser: {"Sim" if user.is_superuser else "Não"}')
            self.stdout.write(f'🏷️ Grupos: {", ".join(groups) if groups else "Nenhum grupo"}')
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Usuário "{username}" não encontrado'))
    
    def add_user_to_group(self, username, group_name):
        """Adiciona usuário a um grupo"""
        try:
            user = User.objects.get(username=username)
            if assign_user_to_group(user, group_name):
                self.stdout.write(self.style.SUCCESS(f'✅ Usuário "{username}" adicionado ao grupo "{group_name}"'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao adicionar usuário ao grupo'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Usuário "{username}" não encontrado'))
    
    def remove_user_from_group(self, username, group_name):
        """Remove usuário de um grupo"""
        try:
            user = User.objects.get(username=username)
            if remove_user_from_group(user, group_name):
                self.stdout.write(self.style.SUCCESS(f'✅ Usuário "{username}" removido do grupo "{group_name}"'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Erro ao remover usuário do grupo'))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Usuário "{username}" não encontrado'))
    
    def create_required_groups(self):
        """Cria grupos necessários"""
        required_groups = [
            ('empresa_admin', 'Administradores da empresa'),
            ('funcionario', 'Funcionários do sistema')
        ]
        
        self.stdout.write(self.style.SUCCESS('🏗️ CRIANDO GRUPOS NECESSÁRIOS'))
        self.stdout.write('=' * 50)
        
        for group_name, description in required_groups:
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Grupo "{group_name}" criado'))
                self.stdout.write(f'   📝 {description}')
            else:
                self.stdout.write(self.style.WARNING(f'ℹ️ Grupo "{group_name}" já existe'))
        
        self.stdout.write('')
        self.stdout.write('💡 Use: python manage.py manage_groups --add-user <username> <group>')
        self.stdout.write('   Exemplo: python manage.py manage_groups --add-user admin empresa_admin')
# Deploy: 2025-11-06 00:04:16
