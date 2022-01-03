"""
WSGI config for askcompany project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 본 wsgi.py 는 서비스 환경에서 자주 사용하므로... askcompany.settings 에 prod 를 붙여서 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askcompany.settings.prod')

application = get_wsgi_application()
