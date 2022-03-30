from django.urls import path
from .views import (UploadPostView, UpdatePostView, DeletePostView, UploadCommentView, UpdateCommentView, DeleteCommentView, 
LikeView, DisLikeView, PostListView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # post
    path('upload/', UploadPostView.as_view(), name='post_upload'),
    path('update/<int:post_pk>/', UpdatePostView.as_view(), name='post_update'),
    path('delete/<int:post_pk>/', DeletePostView.as_view(), name='post_delete'),
    path('list/', PostListView.as_view(), name='post_list'),

    # comment
    path('<int:post_pk>/comment/upload/', UploadCommentView.as_view(), name='comment_upload'),
    path('<int:post_pk>/comment/update/<int:comment_pk>/', UpdateCommentView.as_view(), name='comment_update'),
    path('<int:post_pk>/comment/delete/<int:comment_pk>/', DeleteCommentView.as_view(), name='comment_delete'),

    # reaction
    path('<int:post_pk>/like/', LikeView.as_view(), name='post_like'),
    path('<int:post_pk>/dislike/', DisLikeView.as_view(), name='post_dislike'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)