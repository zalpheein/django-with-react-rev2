from django.urls import path, re_path
from . import views


app_name = 'instagram'

urlpatterns = [
    # 인스타그램의 최상위 url 정의 - localhost:8000/instagram/
    path('', views.index, name="index"),

    path('post/new/', views.post_new, name="post_new"),

    # 이렇게 detail 을 구현 할 경우... 가능한 해당 model 에 get_absolute_url 함수를 정의 할것...
    path('post/<int:pk>/', views.post_detail, name="post_detail"),

    # 좋아요 등록 및 해제... 아래와 같이 별도의 url 을 잡지 않고 javascript 로 대체 처리 가능
    path('post/<int:pk>/like/', views.post_like, name="post_like"),
    path('post/<int:pk>/unlike/', views.post_unlike, name="post_unlike"),

    # comment 등록
    path('post/<int:post_pk>/comment/new/', views.comment_new, name="comment_new"),

    # 만약 username 이 post 이라면?... 그래서 회원가입(signup) 할때, 필수 예약어들은 제외 되어야 함...
    re_path(r'^(?P<username>[\w.@+-]+)/$', views.user_page, name="user_page"),

]