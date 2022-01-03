# 장고앱은 User 모델이 반드시 갖추어야 할 모델이 있으므로 AbstractUser 를 사용
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)


# 새로운 테이블을 만들고 추가 필드를 다음과 같이 정의 할수도 있지만
# 기본 제공 되는 AbstractUser 를 상속받은 class User 에 위와 같이 필드를 추가 할 수도 있음
# 이렇게 필드를 추가 할 경우 common.py(기존의 settings.py) 에 다음 항목 추가
# 보통 DB 관련 이므로... DB 정의부 밑에 선언
#   AUTH_USER_MODEL = "accounts.User"

# class Profile(models.Model):
#     pass





