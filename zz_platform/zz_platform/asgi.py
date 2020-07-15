"""
ASGI config for zz_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this download_file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zz_platform.settings')

application = get_asgi_application()
