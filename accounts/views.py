from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login, PasswordChangeView  # LogoutView
from django.shortcuts import redirect, render
from .forms.forms import SignupForm, ProfileForm

# 로그인 구현
#   순수 자체 제작 함수
#   LoginView() 사용
#   LoginView 를 상속 받은 클래스를 사용
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


@login_required
def password_change(request):
    pass
