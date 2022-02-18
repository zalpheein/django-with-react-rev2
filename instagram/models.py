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
    # author 와 like_user_set 가 충돌이남...DB 단 충돌이 아닌.. ORM 에서의 충돌
    # 특정 user 가 작성한 글 불러오는 방법 2가지
    #   Post.objects.filter(author=user)
    #   user.post_set.all()
    # author 와 like_user_set 가 동일한 명칭(post_set) 의 사용이 충돌 원인
    # 충돌 방지를 위해 related_name 을 정의...
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="my_post_set",
                               on_delete=models.CASCADE)

    # 업로드 파일 경로를 정의
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.CharField(max_length=500)
    # 만약 ManyToManyField(Tag, blank=True) 와 같이 표현 하려면... class Tag 를 class Post 이전에 정의
    tag_set = models.ManyToManyField('Tag', blank=True)
    location = models.CharField(max_length=100, blank=True)

    # author 와 like_user_set 가 충돌이남...DB 단 충돌이 아닌.. ORM 에서의 충돌
    # 특정 user 가 작성한 글 불러오는 방법 2가지
    #   Post.objects.filter(author=user)
    #   user.post_set.all()
    # author 와 like_user_set 가 동일한 명칭(post_set) 의 사용이 충돌 원인
    # 충돌 방지를 위해 related_name 을 정의
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                           related_name="like_post_set",
                                           blank=True)

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

    # 좋아요 상태에 따른 아이콘을 구별 노출 할 목적으로...like_user_set 에 user 가 존재 하는지 질의
    # 절대로 본 함수를 html 에서 직접 사용할 수 없다.. 그래서 templatetags 기술을 이용한다.
    #   templatetags 설명
    #       https://docs.djangoproject.com/ko/4.0/howto/custom-template-tags/
    #       instagram / templatetags 폴더 생성
    #       __init__.py 생성
    #       py 파일 생성 및 내용 구성
    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    class Meta:
        ordering = ['-id']


class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()

    # 사용자 정의하는 모델들의 정렬을 정의 하는 것이 바람직
    class Meta:
        ordering = ['-id']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
