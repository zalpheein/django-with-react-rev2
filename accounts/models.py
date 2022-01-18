# 추가 되는 앱에서 회원 정보 관련 부분은 반드시 갖추어야 할 모델이 있으므로 기본 제공되는 AbstractUser 를 사용.. 추천
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.template.loader import render_to_string


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13,
                                    blank=True,
                                    validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")])
    gender = models.CharField(max_length=1,
                              blank=True,
                              choices=GenderChoices.choices)
    profile = models.ImageField(blank=True,
                                upload_to='accounts/profile/%Y/%m/%d')

    def send_welcome_email(self):
        # 제목과 내용을 하드 코딩 할 수 있으나...템플릿을 활용 하기를 추천...(템플릿 파일명은 무관함)
        # subject = "Instagram 가입을 환영 합니다."
        # content = ""
        subject = render_to_string("accounts/welcome_email_subject.txt", {
            "user": self,
        })
        content = render_to_string("accounts/welcome_email_content.txt", {
            "user": self,
        })

        sender_email = settings.WELCOME_EMAIL_SENDER
        send_mail(subject, content, sender_email, [self.email], fail_silently=False)

    # def save(self, *args, **kwargs):
    #     # 세이브 할때 마다 메일 발송하는 게 아니고...신규 회원 가입 시에만 메일 발송 해야 하므로
    #     is_created = (self.pk == None)
    #     super().save(*args, **kwargs)
    #
    #     if is_created:
    #         # 메일 발송 로직 정의...


#새로운 테이블을 만들고 추가 필드를 다음과 같이 정의 할수도 있지만
# 기본 제공 되는 AbstractUser 를 상속받은 class User 를 만들어 위와 같이 필드를 추가 할 수도 있음... 추천 방식
# 이렇게 필드를 추가 할 경우 common.py(기존의 settings.py) 에 다음 항목 추가
# 보통 DB 관련 이므로... DB 정의부 밑에 선언
#   AUTH_USER_MODEL = "accounts.User"

# class Profile(models.Model):
#     pass





