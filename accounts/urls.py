from django.urls import path, re_path
from . import views

urlpatterns = [
    # 실제 주소는 /accounts/login/ 이다. 또한 settings.LOGIN_URL 의 주소도 동일한 값을 갖음
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_change/', views.password_change, name='password_change'),
    path('signup/', views.signup, name='signup'),
    path('edit/', views.profile_edit, name='profile_edit'),

    # 메인 페이지 우측 하단의 sidebar user follow 목록에서 Follow 버튼 기능 구현 용도
    re_path(r'^(?P<username>[\w.@+-]+)/follow/$', views.user_follow, name="user_follow"),
    re_path(r'^(?P<username>[\w.@+-]+)/unfollow/$', views.user_unfollow, name="user_unfollow"),
]