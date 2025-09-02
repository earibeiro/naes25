from django.core.management.base import BaseCommand
import os
import re


class Command(BaseCommand):
    """
    Comando para corrigir URLs quebradas nos templates
    
    Usage: python manage.py fix_urls
    """
    
    help = 'Corrige URLs quebradas nos templates automaticamente'
    
    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Mostra o que seria alterado sem fazer mudanças')
        parser.add_argument('--backup', action='store_true', help='Cria backup dos arquivos antes de alterar')
    
    def handle(self, *args, **options):
        
        self.stdout.write(self.style.SUCCESS('🔧 CORRIGINDO URLs QUEBRADAS NOS TEMPLATES'))
        self.stdout.write('=' * 60)
        
        # Mapeamento de URLs quebradas → URLs corretas
        url_fixes = {
            'escolha-tipo-cadastro': 'usuarios:cadastro-escolha',
            'create-state': 'state-create',
            'update-state': 'state-update', 
            'delete-state': 'state-delete',
            'create-city': 'city-create',
            'update-city': 'city-update',
            'delete-city': 'city-delete',
        }
        
        templates_dir = 'pages/templates'
        
        if not os.path.exists(templates_dir):
            self.stdout.write(self.style.ERROR(f'Diretório {templates_dir} não encontrado'))
            return
        
        files_changed = 0
        total_fixes = 0
        
        for root, dirs, files in os.walk(templates_dir):
            for file in files:
                if file.endswith('.html'):
                    filepath = os.path.join(root, file)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            original_content = content
                        
                        # Aplicar correções
                        for broken_url, fixed_url in url_fixes.items():
                            pattern = rf"{{% url ['\"]({broken_url})['\"]"
                            replacement = f"{{% url '{fixed_url}'"
                            
                            if re.search(pattern, content):
                                content = re.sub(pattern, replacement, content)
                                total_fixes += 1
                                self.stdout.write(f'  ✓ {broken_url} → {fixed_url} em {os.path.relpath(filepath)}')
                        
                        # Se houve mudanças, salvar arquivo
                        if content != original_content:
                            files_changed += 1
                            
                            if options['dry_run']:
                                self.stdout.write(self.style.WARNING(f'[DRY RUN] Seria alterado: {os.path.relpath(filepath)}'))
                            else:
                                # Backup se solicitado
                                if options['backup']:
                                    backup_path = filepath + '.backup'
                                    with open(backup_path, 'w', encoding='utf-8') as backup_file:
                                        backup_file.write(original_content)
                                    self.stdout.write(f'    💾 Backup criado: {backup_path}')
                                
                                # Salvar arquivo corrigido
                                with open(filepath, 'w', encoding='utf-8') as f:
                                    f.write(content)
                                
                                self.stdout.write(self.style.SUCCESS(f'    📝 Arquivo corrigido: {os.path.relpath(filepath)}'))
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao processar {filepath}: {e}'))
        
        # Resumo
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'📊 RESUMO DA CORREÇÃO:'))
        self.stdout.write(f'   📁 Arquivos alterados: {files_changed}')
        self.stdout.write(f'   🔧 Total de correções: {total_fixes}')
        
        if options['dry_run']:
            self.stdout.write(self.style.WARNING('\n⚠️ DRY RUN - Nenhum arquivo foi realmente alterado'))
            self.stdout.write('Execute sem --dry-run para aplicar as correções')
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ Correções aplicadas com sucesso!'))