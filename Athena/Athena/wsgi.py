# filepath: D:\01_Documentos\02_Faculdade\04_4oAno\NAES\Athena\Athena\wsgi.py

"""
WSGI config for Athena project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# ✅ IMPORTANTE: Usar o path correto do settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Athena.Athena.settings')

application = get_wsgi_application()