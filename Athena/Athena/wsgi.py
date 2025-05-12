# filepath: D:\01_Documentos\02_Faculdade\04_4oAno\NAES\Athena\Athena\wsgi.py

import os
from django.core.wsgi import get_wsgi_application

# Altere esta linha também:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Athena.Athena.settings')
application = get_wsgi_application()