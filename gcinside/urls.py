"""gcinside URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_url_v1_patterns = [
    url('<int:gallery_pk>/post/', include('v1.api.post.urls')),
    url('gallery/', include('v1.api.gallery.urls')),
    url('accounts/', include('accounts.urls')),
]

schema_view_v1 = get_schema_view(
    openapi.Info(
        title="gcinside Open API",
        default_version='v1',
        description="gcinside api document",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="lot8229@kakao.com"),
        license=openapi.License(name="gcinside"),
    ),
    validators=['flex'],  # 'ssv'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,

)


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/',include('dj_rest_auth.urls')),
    path('accounts/',include('allauth.urls')),
    path('accounts/', include('accounts.urls')),

    # Auto DRF API docs
    url(r'^swagger(?P<format>\.json|\.yaml)/v1$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/v1/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/v1/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),

    # 갤러리
    path('gallery/', include('v1.api.gallery.urls')),

    # 게시글
    path('<int:gallery_pk>/post/', include('v1.api.post.urls')),
]
