from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import User


class SignupForm(UserCreationForm):
    # 기존 UserCreationForm 의 Meta 속성을 오버라잇
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'first_name', 'last_name']

    # class Meta:
    #     model = User
    #     fields = ['username', 'password']























