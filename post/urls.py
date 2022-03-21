from django.urls import path
from .views import (UploadPostView, UpdatePostView, DeletePostView, UploadCommentView, UpdateCommentView, DeleteCommentView, 
LikeView, DisLikeView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # post
    path('upload/', UploadPostView.as_view(), name='post_upload'),
    path('update/<int:pk>/', UpdatePostView.as_view(), name='post_update'),
    path('delete/<int:pk>/', DeletePostView.as_view(), name='post_delete'),

    # comment
    path('<int:pk>/comment/upload/', UploadCommentView.as_view(), name='comment_upload'),
    path('<int:pk>/comment/update/<int:comment_pk>/', UpdateCommentView.as_view(), name='comment_update'),
    path('<int:pk>/comment/delete/<int:comment_pk>/', DeleteCommentView.as_view(), name='comment_delete'),

    # reaction
    path('<int:pk>/like/', LikeView.as_view(), name='post_like'),
    path('<int:pk>/dislike/', DisLikeView.as_view(), name='post_dislike'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)