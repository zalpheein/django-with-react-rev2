from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm as AuthPasswordChangeForm,
)
from ..models import User


class SignupForm(UserCreationForm):
    # username 을 제외한 나머지 필드들은 unique 항목이 아님..
    # 그래서 다른 필드들을 생성자(def __init__)에서 unique 로 정의 하는 방법
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    # class Meta 자체도 기존 UserCreationForm 의 Meta 속성을 오버라잇 한 것이므로 이를 상속 받아 인자로 사용
    class Meta(UserCreationForm.Meta):
        # accounts.models.py 에 정의한 사용자 클래스 즉, class User 를 명시적 지정
        # 명시 지정을 하지 않을 경우, django.contrib.auth 에 있는 User 를 사용함.
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 입니다.")
        return email

    # class Meta:
    #     model = User
    #     fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name',
                  'website_url', 'bio', 'phone_number', 'gender']


# 장고 기본 제공 PasswordChangeForm 을 AuthPasswordChangeForm 로 재 명명한
# 클래스를 상속 받은 사용자 정의 class PasswordChangeForm 을 정의
# password2 를 기준으로 동일 비번 입력 여부를 조사
class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password2(self):
        old_password = self.cleaned_data.get('old_password')
        new_password2 = super().clean_new_password2()
        if old_password == new_password2:
            raise forms.ValidationError("새로운 암호는 기존 암호와 다르게 입력해주세요")
        return new_password2



















