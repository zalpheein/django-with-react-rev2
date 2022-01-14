

Git 연동
    인프런 > Do It 장고+부트스트램:파이썬 웹개발의 정석 > 프론트앤드 기초다지기 > HTML 기초... 5:30초

    1. git 에서 신규 repository 생성....django-with-react-rev2

    2. django-with-react-rev2 의 주소를 복사

    3. cmder를 이용하여 로컬에서 git과 연동 할 폴더로 이동
        E:\Dropbox\IT\Projects.Libraries\Python\04.Django\inflearn\django_react

    4. cmder의 해당 폴더에서 "git clone 주소" 명령 실행
        현재 폴더 : E:\Dropbox\IT\Projects.Libraries\Python\04.Django\inflearn\django_react
        입력 명령어 : git clone https://github.com/zalpheein/django-with-react-rev2.git

    5. git과 연동할 폴더가 생성 됨.....django-with-react-rev2 가 "로컬 git 폴더" 임.
        E:\Dropbox\IT\Projects.Libraries\Python\04.Django\inflearn\django_react\django-with-react-rev2

    6. cmder 로 "로컬 git 폴더" 접근
        E:\Dropbox\IT\Projects.Libraries\Python\04.Django\inflearn\django_react\django-with-react-rev2

    7. 가상환경 생성 및 접근
        현재 경로 : E:\Dropbox\IT\Projects.Libraries\Python\04.Django\inflearn\django_react\django-with-react-rev2
        가상환경 생성 : conda create -n django-with-react2 python~=3.0.0
        명령어 : activate django-with-react2

    8. 장고 어드민으로 프로젝트 생성
        현재 경로 : E:\Dropbox\IT\Projects.Libraries\Python\04.Django\inflearn\django_react\django-with-react-rev2
        가상환경 : django-with-react2
        명령어 : django-admin startproject askcompany .

        A)django-admin startproject askcompany 와 B)django-admin startproject askcompany . 의 차이
        A는 django-with-react-rev2 폴더 하위에 askcompany 폴더 생성하고 그 밑에 기본 프로젝트 폴더 askcompany와 manage.py 가 존재
            django-with-react-rev2 폴더
                askcompany 폴더
                    askcompany폴더
                    manage.py
        B는 django-with-react-rev2 폴더 하위에 기본 프로젝트 폴더 askcompany와 manage.py 가 존재
            django-with-react-rev2 폴더
                askcompany폴더
                manage.py

        결과적으로 "로컬 git 폴더" 즉 django-with-react-rev2 폴더를 "프로젝트 폴더"로 지정한 것임.



장고 프로젝트 생성 후 환경 설정
    인프런 > 파이썬/장고 웹서비스 개발 완벽 가이드 with 리액트 > 프로젝트 생성 및 초기 프로젝트 환경 설정.... 강좌 전체



이메일 발송용 Web API 사용
https://docs.sendgrid.com/for-developers/sending-email/django




















