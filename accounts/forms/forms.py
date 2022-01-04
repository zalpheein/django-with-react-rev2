from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import User


class SignupForm(UserCreationForm):
    # username 을 제외한 나머지 필드들은 unique 항목이 아님..
    # 그래서 다른 필드들을 unique 로 정의 하는 방법
    def __call__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True




    # 기존 UserCreationForm 의 Meta 속성을 오버라잇
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    # class Meta:
    #     model = User
    #     fields = ['username', 'password']























