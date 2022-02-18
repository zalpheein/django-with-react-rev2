from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import PostForm, CommentForm
from .models import Post, Tag


@login_required
def index(request):
    # 현재 시간에서 3일 전 시간을 뺀 ==> 즉, 30일전 시간
    timesince = timezone.now() - timedelta(days=30)

    # 팔로잉 한 사람들이 쓴 post 글들의 목록 가져오기
    post_list = Post.objects.all()\
        .filter(
            Q(author__in=request.user.following_set.all()) |    # 팔로잉 한 사람들, 이 경우 내글은 않보임..
            Q(author=request.user)                              # 그래서 내가 작성한 글도 포함...
        )\
        .filter(
            created_at__gte=timesince       # 최근 3일 이내 올라온 글 목록
    )

    # 팔로워/팔로잉 User 목록을 조사
    # User.objects.all() 이렇게 보다는 get_user_model() 을 통해 가져오는 것이 바람직
    suggested_user_list = get_user_model().objects.all()\
        .exclude(pk=request.user.pk)\
        .exclude(pk__in=request.user.following_set.all())[0:3]   # 이미 팔로우 한 사람들은 제외

    # 참고로
    # def index 에서 instagram/index.html 의 _post_form.html 을 호출
    # def post_detail 에서 instagram/post_detail.html 의 _post_form.html 을 호출
    # 하지만 댓글폼의 노출은 오직 instagram/post_detail.html 에서만 노출 됨
    # why? def post_detail 에서만 comment_form 을 인자로 넘기기 때문
    return render(request, "instagram/index.html", {
        "post_list": post_list,
        "suggested_user_list": suggested_user_list,
    })


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

            # 만약 인자로 post 를 사용 하려면, models 에 get_absolute_url 함수가 정의 되어야 함
            # 인자로 post 를 넘기므로... 글 작성 후, post_detail 페이지로 이동
            # return redirect("/")
            return redirect(post)
    else:
        form = PostForm()

    # 당연히 instagram 앱의 templates/instagram/post_form.html 파일이 존재 해야 함....
    return render(request, "instagram/post_form.html", {
        "form": form,
    })


# 다음과 같이 3가지 방식으로 post_detail 를 구현 할 수 있다..여기서는 첫번째 방식으로
# 함수 기반 뷰(순수 자체 제작 함수)
# DetailView() 사용
# DetailView 를 상속 받은 클래스를 사용
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()

    # 참고로
    # def index 에서 instagram/index.html 의 _post_form.html 을 호출
    # def post_detail 에서 instagram/post_detail.html 의 _post_form.html 을 호출
    # 하지만 댓글폼의 노출은 오직 instagram/post_detail.html 에서만 노출 됨
    # why? def post_detail 에서만 comment_form 을 인자로 넘기기 때문
    return render(request, "instagram/post_detail.html", {
        "post": post,
        "comment_form": comment_form,
    })


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # TODO: like 처리 필요
    post.like_user_set.add(request.user)

    messages.success(request, f"포스팅 {post.pk}를 좋아 합니다")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # TODO: unlike 처리 필요
    post.like_user_set.remove(request.user)

    messages.success(request, f"포스팅 {post.pk}의 좋아요를 취소 합니다")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect(comment.post)
    else:
        form = CommentForm()

    return render(request, "instagram/comment_form.html", {
        "form": form,
    })


# 다음과 같이 3가지 방식으로 구현 할 수 있으나 여기서는 "함수 기반 뷰(순수 자체 제작 함수)"로 제작
def user_page(request, username):
    # 현재 로그인 유저를 뽑아 와야 하므로...
    # get_user_model 을 이용하여 username 으로 찾고, 실제 접근이 허용된 사람만 뽑아 옴
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)

    # post_list.count() 는 실제 디비에 질의를 던짐...
    post_list_count = post_list.count()
    # len(post_list) 의 경우, post_list 전체를 가져와서 다시 메모리로 얻지고.. 메모리상의 리스트 개수를 반환..
    # 그래서 post_list 의 개수가 많을 경우 속도 저하 문제 발생 예상

    # 현재 페이지에 접근한 이용자가 page_user 를 팔로우 했다면 ==> is_follow = True
    # 현재 페이지에 접근한 이용자가 page_user 를 언팔로우 했다면 ==> is_unfollow = False
    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    return render(request, "instagram/user_page.html", {
        "page_user": page_user,
        "post_list": post_list,
        "post_list_count": post_list_count,
        "is_follow": is_follow,
    })


















