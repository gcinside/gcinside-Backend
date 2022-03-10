from django.urls import path
from .views import UploadPostView, UpdatePostView, DeletePostView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', UploadPostView.as_view(), name='post_upload'),
    path('update/<int:pk>/', UpdatePostView.as_view(), name='post_update'),
    path('delete/<int:pk>/', DeletePostView.as_view(), name='post_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)