from django import forms
from django.contrib.auth.forms import UserCreationForm
from ..models import User


class SignupForm(UserCreationForm):
    pass
    # class Meta:
    #     model = User
    #     fields = ['username', 'password']























