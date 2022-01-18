from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),      # 실제 주소는 /accounts/login/ 이다. 또한 settings.LOGIN_URL 의 주소도 동일한 값을 갖음
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('edit/', views.profile_edit, name='profile_edit'),
]