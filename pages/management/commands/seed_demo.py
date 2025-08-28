from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from pages.models import Person, Company, Contract, State, City
import random

class Command(BaseCommand):
    help = 'Cria dados de demonstração para o sistema Athena'

    def handle(self, *args, **options):
        self.stdout.write('🌱 CRIANDO DADOS DE DEMONSTRAÇÃO')
        self.stdout.write('=' * 50)
        
        # Criar usuário demo se não existir
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@athena.com',
                'first_name': 'Usuário',
                'last_name': 'Demo'
            }
        )
        
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write(self.style.SUCCESS('✅ Usuário demo criado (demo/demo123)'))
        else:
            self.stdout.write('ℹ️ Usuário demo já existe')
        
        # Criar estados e cidades se não existirem
        try:
            estado_sp, created = State.objects.get_or_create(
                name='São Paulo',
                abbreviation='SP'
            )
            
            cidade_sp, created = City.objects.get_or_create(
                name='São Paulo',
                state=estado_sp
            )
            
            if created:
                self.stdout.write('✅ Estado e cidade criados')
        except Exception as e:
            cidade_sp = None
            self.stdout.write(f'⚠️ Erro ao criar estado/cidade: {e}')
        
        # Criar empresas demo
        empresas_dados = [
            ('Tech Solutions Ltda', 'Tech Solutions'),
            ('Data Corp S.A.', 'Data Corp'),
            ('Innovation Systems Ltda', 'Innovation Systems'),
            ('Digital Services Pro Ltda', 'Digital Pro')
        ]
        
        empresas = []
        for razao_social, nome_fantasia in empresas_dados:
            # Gerar CNPJ fake válido
            cnpj = f'{random.randint(10,99)}.{random.randint(100,999)}.{random.randint(100,999)}/{random.randint(1000,9999)}-{random.randint(10,99)}'
            
            empresa, created = Company.objects.get_or_create(
                corporate_name=razao_social,  # ✅ CAMPO CORRETO
                usuario=user,
                defaults={
                    'trade_name': nome_fantasia,
                    'cnpj': cnpj,
                    'email': f'contato@{nome_fantasia.lower().replace(" ", "")}.com',
                    'phone': f'({random.randint(10,99)}) {random.randint(1000,9999)}-{random.randint(1000,9999)}',
                    'address': f'Rua das Empresas, {random.randint(100,999)}',
                    'city': cidade_sp,
                    'data_processing_purpose': f'Processamento de dados da empresa {nome_fantasia} para fins comerciais e LGPD.'
                }
            )
            empresas.append(empresa)
            if created:
                self.stdout.write(f'✅ Empresa criada: {razao_social}')
        
        # Criar pessoas demo
        pessoas_dados = [
            ('João Silva', 'joao@email.com', '1990-01-15'),
            ('Maria Santos', 'maria@email.com', '1985-03-22'),
            ('Pedro Oliveira', 'pedro@email.com', '1992-07-10'),
            ('Ana Costa', 'ana@email.com', '1988-11-05'),
            ('Carlos Ferreira', 'carlos@email.com', '1995-09-30')
        ]
        
        pessoas = []
        for nome, email, nascimento in pessoas_dados:
            # Gerar CPF fake válido
            cpf = f'{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}'
            
            pessoa, created = Person.objects.get_or_create(
                full_name=nome,  # ✅ CAMPO CORRETO
                usuario=user,
                defaults={
                    'cpf': cpf,
                    'phone': f'({random.randint(10,99)}) {random.randint(1000,9999)}-{random.randint(1000,9999)}',
                    'birth_date': nascimento,
                    'address': f'Rua das Pessoas, {random.randint(100,999)}',
                    'city': cidade_sp,
                    'data_processing_purpose': f'Processamento de dados pessoais de {nome} para fins contratuais e LGPD.'
                }
            )
            pessoas.append(pessoa)
            if created:
                self.stdout.write(f'✅ Pessoa criada: {nome}')
        
        # Criar contratos demo
        contratos_titulos = [
            'Contrato de Prestação de Serviços',
            'Termo de Consentimento LGPD',
            'Acordo de Processamento de Dados',
            'Contrato de Consultoria',
            'Termo de Uso de Dados'
        ]
        
        for i, titulo in enumerate(contratos_titulos):
            empresa = random.choice(empresas) if empresas else None
            pessoa = random.choice(pessoas) if pessoas else None
            
            # Valores possíveis para contract_type (verificar se existe no modelo)
            tipos_contrato = ['SERVICO', 'CONSULTORIA', 'FORNECIMENTO', 'TRABALHO']
            
            contrato, created = Contract.objects.get_or_create(
                title=titulo,
                usuario=user,
                defaults={
                    'description': f'Descrição detalhada do {titulo.lower()}. Este contrato estabelece os termos e condições para o processamento de dados pessoais conforme LGPD.',
                    'company': empresa,
                    'person': pessoa,
                    'start_date': timezone.now().date(),
                    'end_date': timezone.now().date() + timezone.timedelta(days=365),
                    'value': random.randint(1000, 10000),
                    'contract_type': random.choice(tipos_contrato),
                    'data_processing_purpose': f'Finalidade específica para {titulo.lower()}: processamento de dados pessoais necessários para a execução do contrato.',
                    'is_active': random.choice([True, True, True, False])  # 75% ativos
                }
            )
            
            if created:
                self.stdout.write(f'✅ Contrato criado: {titulo}')
        
        # Estatísticas finais
        total_pessoas = Person.objects.filter(usuario=user).count()
        total_empresas = Company.objects.filter(usuario=user).count()
        total_contratos = Contract.objects.filter(usuario=user).count()
        
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('📊 RESUMO DOS DADOS CRIADOS')
        self.stdout.write('=' * 50)
        self.stdout.write(f'👥 Pessoas: {total_pessoas}')
        self.stdout.write(f'🏢 Empresas: {total_empresas}')
        self.stdout.write(f'📋 Contratos: {total_contratos}')
        self.stdout.write(f'👤 Usuário: {user.username} (senha: demo123)')
        self.stdout.write('\n🎉 Dados de demonstração criados com sucesso!')
        self.stdout.write('💡 Use estes dados para testar o sistema.')