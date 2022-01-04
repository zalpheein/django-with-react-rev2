from django import forms
form ..models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']






















