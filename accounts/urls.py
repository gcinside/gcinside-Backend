from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('github/login/', views.github_login, name='github_login'),
    # path('github/callback/', views.github_callback, name='github_callback'),
    # path('github/login/finish/', views.GithubLogin.as_view(),
    #      name='github_login_todjango'),

    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(),
         name='google_login_todjango'),
    path('github/login/', views.github_login, name='github_login'),
    path('github/callback/', views.github_callback, name='github_callback'),
    path('github/login/finish/', views.GithubLogin.as_view(), name='github_login_todjango'),

    path('user/profile/username/<username>/', views.UpdateUsername.as_view(), name='update_username'),
    path('user/profile/image/<username>/', views.UpdateProfileImage.as_view(), name='update_profileImage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)