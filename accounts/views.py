from django.contrib import messages
from django.shortcuts import redirect, render
from .forms.forms import SignupForm


def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # 프런트에 message 내용이 노출 되어야 함으로...
            # askcompany/templates/layout.html 에 관련 내용을 삽입 해야 함
            messages.success(request, "회원가입 환영합니다.")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()

    return render(request, 'accounts/signup_form.html', {
                        'form': form,
                    }
                )
