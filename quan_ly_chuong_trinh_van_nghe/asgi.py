"""
ASGI config for quan_ly_chuong_trinh_van_nghe project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quan_ly_chuong_trinh_van_nghe.settings')

application = get_asgi_application()
