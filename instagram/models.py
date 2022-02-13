# 정규표현식 사용을 선언
import re
from django.conf import settings
from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 업로드 파일 경로를 정의
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.CharField(max_length=500)
    # 만약 ManyToManyField(Tag, blank=True) 와 같이 표현 하려면... class Tag 를 class Post 이전에 정의
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100, blank=True)



    def __str__(self):
        return self.caption

    # 신규 포스트 저장 하면서... caption 에서 # 이 붙은 문자을 찾아 Tag 대상을 뽑아 내는 함수
    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힝]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    # urls 에 post 에 대한 detail 경로를 정의 할 경우... model 에 get_absolute_url 함수를 가능할 정의 할것
    def get_absolute_url(self):
        # return reverse("instagram:post_detail", kwargs={"pk": self.pk}) # 동일한 코드
        return reverse("instagram:post_detail", args=[self.pk])     # 동일한 코드


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
