from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import PostForm
from .models import Tag


@login_required
def post_new(request):
    if request.method == "POST":
        # PostForm 에 사용자 입력 데이터를 채우라는 의미 +++++++++++++++
        form = PostForm(request.POST, request.FILES)

        # 그리고 나서 form 을 검증
        if form.is_valid():
            # post = form.save()
            # form 의 fields 에서 author 를 제외 하였기에 commit=False 처리하여 즉시 저장을 제한함
            # 왜? 필수 입력값인 author 와 tage_set 값을 지정 해야 하므로
            post = form.save(commit=False)

            # author 값 지정하기
            post.author = request.user

            # post 를 저장을 먼저 하고 tag 를 저장 해야 함
            post.save()

            # tag_set 값 지정하기
            # post.extract_tag_list() 가 list 형태 이므로 * 을 붙여서 한번에 처리
            # 단, post 저장이 선행 되어야 함...
            post.tag_set.add(*post.extract_tag_list())

            messages.success(request, "포스팅을 저장 하였습니다.")

            # 만약 인자로 post 를 사용 하려면, models에 get_absolute_url 함수가 정의 되어야 함
            return redirect("/")
    else:
        form = PostForm()

    # 당연히 instagram 앱의 templates/instagram/post_form.html 파일이 존재 해야 함....
    return render(request, "instagram/post_form.html", {
        "form": form,
    })
