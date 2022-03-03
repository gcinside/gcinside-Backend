from unicodedata import name
from django.urls import path
from .views import UploadPostView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', UploadPostView.as_view(), name='post_upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)