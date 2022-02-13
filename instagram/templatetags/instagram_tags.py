
# 템플릿 태그 정의 및 사용법
# https://docs.djangoproject.com/ko/4.0/howto/custom-template-tags/

from django import template

register = template.Library()


@register.filter
def is_like_user(post, user):
    return post.is_like_user(user)