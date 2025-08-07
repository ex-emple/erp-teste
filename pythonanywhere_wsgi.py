"""
Configuration WSGI pour PythonAnywhere
"""
import os
import sys

# Configuration du chemin - REMPLACEZ 'votrenom' par votre nom d'utilisateur PythonAnywhere
path = '/home/votrenom/mini-erp-docteur'
if path not in sys.path:
    sys.path.append(path)

# Configuration Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_pythonanywhere'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
