from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 업로드 파일 경로를 정의
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.CharField(max_length=500)
    # 만약 ManyToManyField(Tag, blank=True) 와 같이 표현 하려면... class Tag 를 class Post 이전에 정의
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.caption



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
