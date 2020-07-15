"""
WSGI config for zz_platform project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this download_file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zz_platform.settings')

application = get_wsgi_application()
