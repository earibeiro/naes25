"""
Comando Django para corrigir TODOS os templates de uma vez
"""
import os
import re
from django.core.management.base import BaseCommand
from pathlib import Path


class Command(BaseCommand):
    help = 'Corrige TODOS os problemas de URLs nos templates automaticamente'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 CORREÇÃO COMPLETA DE TEMPLATES'))
        self.stdout.write('=' * 80)

        # ✅ MAPEAMENTO COMPLETO DE TODAS AS URLS QUEBRADAS
        url_fixes = {
            # 1️⃣ URLs de cadastro (múltiplas variações)
            r"{% url 'cadastro' %}": "{% url 'usuarios:cadastro-escolha' %}",
            r"{% url 'escolha_tipo_cadastro' %}": "{% url 'usuarios:cadastro-escolha' %}",
            r"{% url 'escolha-tipo-cadastro' %}": "{% url 'usuarios:cadastro-escolha' %}",
            
            # 2️⃣ URLs de login/logout sem namespace
            r"{% url 'login' %}": "{% url 'usuarios:login' %}",
            r"{% url 'logout' %}": "{% url 'usuarios:logout' %}",
            
            # 3️⃣ URLs de senha sem namespace
            r"{% url 'password_reset' %}": "{% url 'usuarios:password_reset' %}",
            r"{% url 'password_change' %}": "{% url 'usuarios:password_change' %}",
            
            # 4️⃣ URLs antigas de State
            r"{% url 'create-state' %}": "{% url 'state-create' %}",
            r"{% url 'update-state' ": "{% url 'state-update' ",
            r"{% url 'delete-state' ": "{% url 'state-delete' ",
            r"{% url 'detail-state' ": "{% url 'state-detail' ",
            
            # 5️⃣ URLs antigas de City
            r"{% url 'create-city' %}": "{% url 'city-create' %}",
            r"{% url 'update-city' ": "{% url 'city-update' ",
            r"{% url 'delete-city' ": "{% url 'city-delete' ",
            r"{% url 'detail-city' ": "{% url 'city-detail' ",
        }

        # Diretórios a processar
        directories = [
            Path('pages/templates'),
            Path('usuarios/templates'),
        ]

        total_files = 0
        total_fixes = 0

        for directory in directories:
            if not directory.exists():
                self.stdout.write(self.style.WARNING(f'⚠️ Diretório {directory} não encontrado'))
                continue

            self.stdout.write(f'\n📁 Processando: {directory}')
            self.stdout.write('-' * 80)

            files_changed, fixes_count = self._process_directory(directory, url_fixes)
            total_files += files_changed
            total_fixes += fixes_count

        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(self.style.SUCCESS('✅ CORREÇÃO COMPLETA FINALIZADA'))
        self.stdout.write(f'📝 Total de arquivos modificados: {total_files}')
        self.stdout.write(f'🔧 Total de correções aplicadas: {total_fixes}')

    def _process_directory(self, directory, url_fixes):
        """Processa todos os arquivos HTML em um diretório"""
        files_changed = 0
        total_fixes = 0

        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.html'):
                    filepath = Path(root) / filename
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(f'❌ Erro ao ler {filepath}: {e}')
                        )
                        continue
                    
                    original_content = content
                    file_fixes = 0

                    # Aplicar todas as correções
                    for old_pattern, new_pattern in url_fixes.items():
                        matches = list(re.finditer(old_pattern, content))
                        if matches:
                            content = re.sub(old_pattern, new_pattern, content)
                            fix_count = len(matches)
                            file_fixes += fix_count
                            
                            # Exibir apenas se houver correções
                            relative_path = filepath.relative_to(directory.parent)
                            self.stdout.write(
                                f'  🔧 {relative_path}: '
                                f'{fix_count}x "{old_pattern[:30]}..." → "{new_pattern[:30]}..."'
                            )

                    # Salvar se houve mudanças
                    if content != original_content:
                        try:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(content)
                            
                            files_changed += 1
                            total_fixes += file_fixes
                            
                            relative_path = filepath.relative_to(directory.parent)
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'✅ {relative_path}: {file_fixes} correções salvas'
                                )
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f'❌ Erro ao salvar {filepath}: {e}')
                            )

        return files_changed, total_fixes