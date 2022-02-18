from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # __all__ 의 경우, author 도 선택 할 수 있는 UI가 제공 됨
        # 이를 해결하기 위해 특정 필드만 UI에 노출 되도록
        # 그러므로 필수 입력값인 author 의 처리는 views 의 post_new 함수에서 처리 해야...
        fields = ['photo', 'caption', 'location']

        # 특정 필드의 UI 모습을 widget 을 이용하여 변경
        widgets = {
            "caption": forms.Textarea,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        widgets = {
            "message": forms.Textarea(attrs={"rows": 2}),
        }


