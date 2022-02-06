from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import RedirectView   # TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),

    # 사용자가 localhost:8000/instagram/ 요청 시... instagram.urls 의 path('', views.index, name="index") 가 호출
    path('instagram/', include('instagram.urls')),

    # 사용자가 localhost:8000/ 요청 시에도 localhost:8000/instagram/ 이 호출 되도록 변경+++++
    # 즉 바로 위의 경로인 path('instagram/', include('instagram.urls')) 가 호출 됨
    # path('', login_required(TemplateView.as_view(template_name='root.html')), name='root')
    path('', RedirectView.as_view(pattern_name='instagram:index'), name='root')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
