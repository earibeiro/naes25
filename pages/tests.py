from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Person, Company, State, City

class GroupProtectionTest(TestCase):
    """
    Testes para proteção por grupos e escopo por owner
    """
    
    def setUp(self):
        # Usar get_or_create para evitar erro de duplicata
        self.admin_group, created = Group.objects.get_or_create(name='empresa_admin')
        self.user_group, created = Group.objects.get_or_create(name='funcionario')
        
        # Criar usuários
        self.admin_user = User.objects.create_user(
            username='admin', 
            password='pass123'
        )
        self.admin_user.groups.add(self.admin_group)
        
        self.regular_user = User.objects.create_user(
            username='user', 
            password='pass123'
        )
        self.regular_user.groups.add(self.user_group)
        
        # CRIAR USUÁRIO ADICIONAL para teste de criação
        self.test_user = User.objects.create_user(
            username='testuser', 
            password='pass123'
        )
        self.test_user.groups.add(self.user_group)
        
        self.no_group_user = User.objects.create_user(
            username='nogroup', 
            password='pass123'
        )
        
        # Criar dados de teste
        self.state = State.objects.create(name='São Paulo', abbreviation='SP')
        self.city = City.objects.create(name='São Paulo', state=self.state)
        
        # Criar registros para admin_user
        self.admin_person = Person.objects.create(
            full_name='Admin Person',
            cpf='123.456.789-00',
            phone='11999999999',
            birth_date='1990-01-01',
            address='Rua A, 123',
            city=self.city,
            data_processing_purpose='Teste',
            usuario=self.admin_user
        )
        
        # Criar registros para regular_user
        self.user_person = Person.objects.create(
            full_name='User Person',
            cpf='987.654.321-00',
            phone='11888888888',
            birth_date='1990-01-01',
            address='Rua B, 456',
            city=self.city,
            data_processing_purpose='Teste',
            usuario=self.regular_user
        )
        
        self.client = Client()
    
    def test_no_group_user_redirected(self):
        """
        Usuário sem grupo correto deve ser redirecionado (302/login)
        """
        self.client.login(username='nogroup', password='pass123')
        response = self.client.get(reverse('person-list'))
        self.assertEqual(response.status_code, 302)
    
    def test_user_cannot_see_other_user_records(self):
        """
        Usuário não deve ver registros de outro usuário
        """
        self.client.login(username='user', password='pass123')
        response = self.client.get(reverse('person-list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User Person')
        self.assertNotContains(response, 'Admin Person')
    
    def test_user_cannot_edit_other_user_records(self):
        """
        Usuário não deve poder editar registros de outro usuário
        """
        self.client.login(username='user', password='pass123')
        
        response = self.client.get(
            reverse('update-person', kwargs={'pk': self.admin_person.pk})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_admin_can_access_all_views(self):
        """
        Admin deve ter acesso a todas as views
        """
        self.client.login(username='admin', password='pass123')
        
        response = self.client.get(reverse('person-list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('company-list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('state-list'))
        self.assertEqual(response.status_code, 200)
    
    def test_regular_user_cannot_access_admin_views(self):
        """
        Usuário regular não deve acessar views de admin
        """
        self.client.login(username='user', password='pass123')
        
        response = self.client.get(reverse('state-list'))
        self.assertEqual(response.status_code, 302)
    
    def test_owner_scope_in_create(self):
        """
        Testar se o owner é atribuído corretamente na criação
        """
        # USAR USUÁRIO SEM PERSON EXISTENTE
        self.client.login(username='testuser', password='pass123')
        
        data = {
            'full_name': 'New Person',
            'cpf': '111.222.333-44',
            'phone': '11777777777',
            'birth_date': '1990-01-01',
            'address': 'Rua C, 789',
            'city': self.city.id,
            'data_processing_purpose': 'Teste criação'
        }
        
        response = self.client.post(reverse('create-person'), data)
        self.assertEqual(response.status_code, 302)
        
        new_person = Person.objects.get(cpf='111.222.333-44')
        self.assertEqual(new_person.usuario, self.test_user)

# Deploy: 2025-11-06 00:04:16
