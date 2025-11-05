from django.core.management.base import BaseCommand
import os
import re
from pathlib import Path


class Command(BaseCommand):
    help = 'Corrige URLs quebradas nos templates automaticamente'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 CORRIGINDO URLs QUEBRADAS NOS TEMPLATES'))
        self.stdout.write('=' * 60)

        # Mapeamento de URLs quebradas → URLs corretas
        url_fixes = {
            # ✅ ADICIONAR ESTA LINHA
            r"{% url 'cadastro' %}": "{% url 'usuarios:cadastro-escolha' %}",
            
            # URLs do sistema de usuários
            r"{% url 'escolha_tipo_cadastro' %}": "{% url 'usuarios:cadastro-escolha' %}",
            r"{% url 'escolha-tipo-cadastro' %}": "{% url 'usuarios:cadastro-escolha' %}",
            
            # URLs antigas de State (se existirem)
            r"{% url 'create-state' %}": "{% url 'state-create' %}",
            r"{% url 'update-state' ": "{% url 'state-update' ",
            r"{% url 'delete-state' ": "{% url 'state-delete' ",
            r"{% url 'detail-state' ": "{% url 'state-detail' ",
            
            # URLs antigas de City (se existirem)
            r"{% url 'create-city' %}": "{% url 'city-create' %}",
            r"{% url 'update-city' ": "{% url 'city-update' ",
            r"{% url 'delete-city' ": "{% url 'city-delete' ",
            r"{% url 'detail-city' ": "{% url 'city-detail' ",
            
            # Corrigir views.home para views.HomeView
            r"views\.home": "views.HomeView.as_view()",
        }

        templates_dir = Path('pages/templates')
        usuarios_templates_dir = Path('usuarios/templates')

        if not templates_dir.exists():
            self.stdout.write(self.style.ERROR(f'Diretório {templates_dir} não encontrado'))
            return

        files_changed = 0
        total_fixes = 0

        # Processar templates do app pages
        files_changed, total_fixes = self._process_directory(
            templates_dir, url_fixes, files_changed, total_fixes
        )

        # Processar templates do app usuarios (se existir)
        if usuarios_templates_dir.exists():
            files_changed, total_fixes = self._process_directory(
                usuarios_templates_dir, url_fixes, files_changed, total_fixes
            )

        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'✅ CONCLUÍDO!'))
        self.stdout.write(f'📝 Arquivos modificados: {files_changed}')
        self.stdout.write(f'🔧 Total de correções: {total_fixes}')

    def _process_directory(self, directory, url_fixes, files_changed, total_fixes):
        """Processa todos os arquivos HTML em um diretório"""
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.html'):
                    filepath = Path(root) / filename
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    file_fixes = 0

                    # Aplicar todas as correções
                    for old_pattern, new_pattern in url_fixes.items():
                        matches = re.findall(old_pattern, content)
                        if matches:
                            content = re.sub(old_pattern, new_pattern, content)
                            fix_count = len(matches)
                            file_fixes += fix_count
                            self.stdout.write(
                                f'  🔧 {filepath.relative_to(directory.parent)}: '
                                f'{fix_count}x "{old_pattern}" → "{new_pattern}"'
                            )

                    # Salvar se houve mudanças
                    if content != original_content:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        files_changed += 1
                        total_fixes += file_fixes
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ {filepath.name}: {file_fixes} correções aplicadas')
                        )

        return files_changed, total_fixes