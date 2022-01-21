from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import PostForm


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()

            messages.success(request, "포스팅을 저장 하였습니다.")

            # 만약 인자로 post 를 사용 하려면, models에 get_absolute_url 함수가 정의 되어야 함
            return redirect("/")
    else:
        form = PostForm()

    # 당연히 instagram 앱의 templates/instagram/post_form.html 파일이 존재 해야 함....
    return render(request, "instagram/post_form.html", {
        "form": form,
    })
