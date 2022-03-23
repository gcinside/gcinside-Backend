from django.urls import path
from .views import UploadGalleryView

urlpatterns = [
    path('upload/', UploadGalleryView.as_view(), name='upload_gallery'),
]