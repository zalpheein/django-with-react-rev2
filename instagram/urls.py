from django.urls import path, re_path
from . import views


app_name = 'instagram'

urlpatterns = [
    path('post/new/', views.post_new, name="post_new"),

    # 이렇게 detail 을 구현 할 경우... 가능한 해당 model 에 get_absolute_url 함수를 정의 할것...
    path('post/<int:pk>/', views.post_detail, name="post_detail"),

    # 만약 username 이 post 이라면?... 그래서 회원가입(signup) 할때, 필수 예약어들은 제외 되어야 함...
    re_path(r'^(?P<username>[\w.@+-]+)/]', views.user_page, name="user_page"),

]