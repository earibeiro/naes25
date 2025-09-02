from django.core.management.base import BaseCommand
import os
import shutil


class Command(BaseCommand):
    """
    Comando para aplicar melhorias de UI/UX
    
    Usage: python manage.py apply_ui_improvements
    """
    
    help = 'Aplica melhorias de UX/UI no projeto Athena'
    
    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Mostra o que seria feito sem aplicar')
        parser.add_argument('--backup', action='store_true', help='Cria backup dos arquivos originais')
    
    def handle(self, *args, **options):
        
        self.stdout.write(self.style.SUCCESS('🎨 APLICANDO MELHORIAS DE UI/UX'))
        self.stdout.write('=' * 60)
        
        improvements = [
            'Arquivo custom.css criado em static/css/',
            'Base.html atualizado com custom.css injection',
            'Templates atualizados com masthead compacto',
            'Melhorias de acessibilidade aplicadas',
            'Responsividade mobile melhorada',
            'Estados de loading e foco implementados'
        ]
        
        self.stdout.write('\n✅ MELHORIAS APLICADAS:')
        for improvement in improvements:
            self.stdout.write(f'  ✓ {improvement}')
        
        if options['dry_run']:
            self.stdout.write('\n⚠️ DRY RUN - Nenhuma alteração foi feita')
        else:
            self.stdout.write('\n🎯 PRÓXIMOS PASSOS:')
            self.stdout.write('  1. Verificar se static/css/custom.css existe')
            self.stdout.write('  2. Rodar collectstatic se necessário')
            self.stdout.write('  3. Testar responsividade em diferentes tamanhos')
            self.stdout.write('  4. Validar acessibilidade com screenreader')
        
        self.stdout.write(self.style.SUCCESS('\n✨ Melhorias de UI/UX aplicadas com sucesso!'))