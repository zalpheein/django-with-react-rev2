#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # asgi.py + wsgi.py + manage.py 모두 수정 해야 함....why? 기존의 settings.py 를
    # askcompany.settings 폴더 내로 이동 하엿기 때문... 더군다나 파일명을 변경 하기까지 했음...

    # 프로그램이 시작 했을 때, 환경변수 목록에서(os.environ) DJANGO_SETTINGS_MODULE 모듈이 없다면,
    # askcompany.settings.dev 값을 대신 환경변수로 지정 하겠다라는 의미
    # askcompany.settings은 현재 폴더를 의미... __init__.py 가 현재 폴더 내의 파일들을 읽어 올수 있게 함

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askcompany.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
