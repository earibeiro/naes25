from django.core.management.base import BaseCommand
from django.urls import reverse, NoReverseMatch
import os
import re


class Command(BaseCommand):
    """
    Comando para verificar URLs nos templates
    
    Usage: python manage.py check_urls
    """
    
    help = 'Verifica URLs nos templates e encontra links quebrados'
    
    def handle(self, *args, **options):
        
        self.stdout.write(self.style.SUCCESS('🔍 VERIFICANDO URLs NOS TEMPLATES'))
        self.stdout.write('=' * 60)
        
        # URLs que sabemos que funcionam
        working_urls = [
            'index', 'about', 'home',
            'person-list', 'person-create',
            'company-list', 'company-create', 
            'contract-list', 'contract-create',
            'state-list', 'city-list',
            'contrato-draft-start',
            'login', 'logout',
            'usuarios:cadastro-escolha',
            'usuarios:change-password',
            'auditoria:activity-logs'
        ]
        
        # URLs problemáticas encontradas nos templates
        problematic_urls = [
            'escolha-tipo-cadastro',  # Deve ser usuarios:cadastro-escolha
            'about-en',               # Adicionar se necessário
        ]
        
        self.stdout.write('\n✅ URLs FUNCIONAIS:')
        for url_name in working_urls:
            try:
                url = reverse(url_name)
                self.stdout.write(f'  ✓ {url_name} → {url}')
            except NoReverseMatch:
                self.stdout.write(self.style.ERROR(f'  ❌ {url_name} → ERRO'))
        
        self.stdout.write('\n⚠️ URLs PROBLEMÁTICAS:')
        for url_name in problematic_urls:
            self.stdout.write(f'  ⚠️ {url_name} → PRECISA SER CORRIGIDO')
        
        self.stdout.write('\n📋 CORREÇÕES SUGERIDAS:')
        self.stdout.write('  1. Adicionar rota /about/ → about-en')
        self.stdout.write('  2. Corrigir escolha-tipo-cadastro → usuarios:cadastro-escolha')
        self.stdout.write('  3. Verificar todos os templates para consistência')
        
        # Buscar por padrões {% url %} nos templates
        self.stdout.write('\n🔎 BUSCANDO PADRÕES {% url %} NOS TEMPLATES...')
        self.find_url_patterns()
    
    def find_url_patterns(self):
        """Busca padrões {% url %} nos templates"""
        templates_dir = 'pages/templates'
        
        if not os.path.exists(templates_dir):
            self.stdout.write(self.style.WARNING(f'Diretório {templates_dir} não encontrado'))
            return
        
        url_pattern = re.compile(r"{% url ['\"]([^'\"]+)['\"]")
        
        for root, dirs, files in os.walk(templates_dir):
            for file in files:
                if file.endswith('.html'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            urls_found = url_pattern.findall(content)
                            
                            if urls_found:
                                rel_path = os.path.relpath(filepath)
                                self.stdout.write(f'\n📄 {rel_path}:')
                                
                                for url_name in set(urls_found):
                                    try:
                                        reverse(url_name)
                                        self.stdout.write(f'    ✓ {url_name}')
                                    except NoReverseMatch:
                                        self.stdout.write(self.style.ERROR(f'    ❌ {url_name} → QUEBRADO'))
                                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao ler {filepath}: {e}'))
# Deploy: 2025-11-06 00:04:16
