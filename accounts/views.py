from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# 콤마(,) 로 구분 되는 모든 값들을 튜플(tuple)로 처리 가능
# from django.contrib.auth.views import LoginView, logout_then_login, PasswordChangeView as AuthPasswordChangeView
from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordChangeView as AuthPasswordChangeView,
)
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from .forms.forms import SignupForm, ProfileForm, PasswordChangeForm
from .models import User

# 로그인 구현
#   순수 자체 제작 함수
#   LoginView() 사용 <--- 이 방법을 사용함
#   LoginView 를 상속 받은 클래스를 사용 <-- 이 방법은 [비번 변경] 방식을 참조 할 것
login = LoginView.as_view(template_name="accounts/login_form.html")


# logout = LogoutView.as_view()
def logout(request):
    messages.success(request, "로그아웃 되었습니다.")
    return logout_then_login(request)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()

            # 회원가입 환영 메시지 처리...
            # 프런트에 message 내용이 노출 되어야 함으로...
            # askcompany/templates/layout.html 에 관련 내용을 삽입 해야 함
            messages.success(request, "회원가입 환영합니다.")

            # 회원가입과 동시에 로그인 처리....
            auth_login(request, signed_user)

            # 회원가입 시 이메일 발송
            # 여기에 회원가입 환영 이메일을 보내는 기능을 정의 하거나 함수를 호출 할수 있음
            # 메일 발송 함수 정의는 views.py 에 정의 하는 것보다는
            #   장고의 시그널을 사용 할수도 있고...
            #   models.py 의 class User 에서 함수를 정의 할수도 있다...본 방식을 추천
            #   회원가입과 메일 발송이 연속적이어서.. 회원가입 처리가 늦어지는 현상 발생
            #   Celery 를 활용 할것을 제안함...
            signed_user.send_welcome_email()

            # next 인자의 값을 알아오는데.. next 인자가 없을 경우 두 번째 인자를 반환
            next_url = request.GET.get('next', '/')

            return redirect(next_url)
    else:
        form = SignupForm()

    return render(request, 'accounts/signup_form.html', {
        'form': form,
    }
                  )


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 수정 하였습니다.")
            return redirect('profile_edit')

    else:
        form = ProfileForm(instance=request.user)

    return render(request, "accounts/profile_edit_form.html", {
        "form": form
    })


# 장고 기본 제공 PasswordChangeView 를 활용하여 사용자 정의형으로 재가공 하여 비번을 변경하는 로직
# class PasswordChangeView 은 AuthPasswordChangeView 를 상속 받아 생성
# AuthPasswordChangeView 은 장고 기본 제공 PasswordChangeView 의 사용자 정의 이름
class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    # 비번 변경 성공 시 랜당할 랜딩 페이지 주소
    # 비번 변경에 사용할 템플릿 지정
    # 비번 변경에 사용할/적용할 로직을 담음 폼 클래스 지정
    success_url = reverse_lazy("password_change")
    template_name = "accounts/password_change_form.html"
    form_class = PasswordChangeForm

    # 비번 변경 시, 사용자에게 변경이 완료 되었다는 메시지 노출하기 위해
    # 미 해결 문제 : 구 암호와 신 암호를 동일하게 입력 해도 암호 변경이 성공됨.. 이를 해결 해야함
    # 그래서 위에 form_class = PasswordChangeForm 라인이 추가 됨
    def form_valid(self, form):
        messages.success(self.request, "암호를 변경했습니다.")

        # super().form_valid(form) 가 호출 되면서 내부적으로 비번이 변경 되어짐
        # https://github.com/django/django/blob/main/django/contrib/auth/views.py 의 356번째 라인 참조
        return super().form_valid(form)


password_change = PasswordChangeView.as_view()

# 팔로우 할 대상 username 을 인자로 넘겨야
@login_required
def user_follow(request, username):
    follow_user = get_object_or_404(User, username=username, is_active=True)

    messages.success(request, f"{follow_user}님을 팔로우 했습니다.")

    # 팔로우 처리 완료 후, 요청 페이지로 돌아감... 이전 페이지는 레퍼러를 참조하여 알아냄
    # 레퍼러가 있으면 가져오고 없으면 root 를 반환
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


# 언팔로우 할 대상 username 을 인자로 넘겨야
@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username, is_active=True)

    messages.success(request, f"{unfollow_user}님을 언팔로우 했습니다.")

    # 언팔로우 처리 완료 후, 요청 페이지로 돌아감... 이전 페이지는 레퍼러를 참조하여 알아냄
    # 레퍼러가 있으면 가져오고 없으면 root 를 반환
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)



