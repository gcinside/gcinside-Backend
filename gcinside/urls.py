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
import rest_auth.registration.views
from django.contrib import admin
from django.urls import path, include
from rest_auth.registration.views import RegisterView
from rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView,
    PasswordResetView, PasswordResetConfirmView
)
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_url_v1_patterns = [
    url('rest-auth/login', LoginView.as_view(), name='rest_login'),
    url('rest-auth/logout', LogoutView.as_view(), name='rest_logout'),
    url('rest-auth/password/change', PasswordChangeView.as_view(), name='rest_password_change'),

    # 회원가입
    url('rest-auth/registration', RegisterView.as_view(), name='rest_register'),
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

    # 로그인
    path('rest-auth/login', LoginView.as_view(), name='rest_login'),
    path('rest-auth/logout', LogoutView.as_view(), name='rest_logout'),
    path('rest-auth/password/change', PasswordChangeView.as_view(), name='rest_password_change'),

    # 회원가입
    path('rest-auth/registration', RegisterView.as_view(), name='rest_register'),

    # Auto DRF API docs
    url(r'^swagger(?P<format>\.json|\.yaml)/v1$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/v1/$', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/v1/$', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]
