"""
ASGI config for askcompany project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# 본 asgi.py 는 서비스 환경에서 자주 사용하므로... askcompany.settings 에 prod 를 붙여서 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askcompany.settings.prod')

application = get_asgi_application()
