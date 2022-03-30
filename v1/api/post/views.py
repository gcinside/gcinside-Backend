from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils import timezone

import logging.config
import logging
from gcinside.settings import DEFAULT_LOGGING

from .serializers import PostSerializer, CommentSerializer, LikeSerialzier, DisLikeSerializer
from .models import Post, Comment
from .pagination import PostPagination

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logging.config.dictConfig(DEFAULT_LOGGING)
# Create your views here.
# post
class UploadPostView(GenericAPIView):
    serializer_class = PostSerializer

    @permission_classes(IsAuthenticated, )
    def post(self, request, gallery_pk):
        if request.user.is_authenticated:
            serializer = PostSerializer(
                data = {
                    'gallery' : gallery_pk,
                    'author' : request.user.id,
                    'title' : request.POST['title'],
                    'content' : request.POST['content'],
                    'image' : request.FILES.get('image', None),
                    'created_at' : timezone.now(),
                }
            )

            if (serializer.is_valid()):
                serializer.save()

                return JsonResponse({'message' : 'Upload success'}, status=201)
            logging.info(serializer.data)
            return JsonResponse({'message' : 'Bad request'}, status=400)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

class UpdatePostView(GenericAPIView):
    serializer_class = PostSerializer

    @permission_classes(IsAuthenticated, )
    def put(self, request, gallery_pk, post_pk):
        if request.user.is_authenticated:
            posting = Post.objects.get(id=post_pk)

            if posting.author == request.user:
                serializer = PostSerializer(
                    posting,
                    data = {
                        'gallery' : gallery_pk,
                        'author' : request.user.id,
                        'title' : request.POST['title'],
                        'content' : request.POST['content'],
                        'image' : request.FILES.get('image', None),
                        'created_at' : timezone.now(),
                    }
                )
    
                if serializer.is_valid():
                    serializer.save()
    
                    return JsonResponse({'message' : 'Update success'}, status=201)
                return JsonResponse({'message' : 'Bad request'}, status=400)
            else :
                return JsonResponse({'message' : 'different user'}, status=401)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

class DeletePostView(GenericAPIView):
    serializer_class = PostSerializer

    @permission_classes(IsAuthenticated, )
    def delete(self, request, gallery_pk, post_pk):
        if request.user.is_authenticated:
            posting = Post.objects.get(id=post_pk)

            if posting.author == request.user:
                posting.delete()

                return JsonResponse({'message' : 'Delete success'}, status=200)
            return JsonResponse({'message' : 'different user'}, status=401)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

class PostListView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination

# comment
class UploadCommentView(GenericAPIView):
    serializer_class = CommentSerializer

    @permission_classes(IsAuthenticated, )
    def post(self, request, gallery_pk, post_pk):
        if request.user.is_authenticated:
            serializer = CommentSerializer(
                data = {
                    'post' : post_pk,
                    'user' : request.user.id,
                    'content' : request.POST['content'],
                    'created_at' : timezone.now(),
                }
            )

            if serializer.is_valid():
                serializer.save()

                return JsonResponse({'message' : 'Upload success'}, status=201)
            return JsonResponse({'message' : 'Bad request'}, status=400)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

class UpdateCommentView(GenericAPIView):
    serializer_class = CommentSerializer

    @permission_classes(IsAuthenticated, )
    def put(self, request, gallery_pk, post_pk, comment_pk):
        if request.user.is_authenticated:
            comment = Comment.objects.get(id=comment_pk)

            if comment.user == request.user:
                serializer = CommentSerializer(
                    comment,
                    data = {
                        'post' : post_pk,
                        'user' : request.user.id,
                        'content' : request.POST['content'],
                        'created_at' : timezone.now(),
                    }
                )

                if serializer.is_valid():
                    serializer.save()

                    return JsonResponse({'message' : 'Update success'}, status=201)
                return JsonResponse({'message' : 'Bad request'}, status=400)
            else :
                return JsonResponse({'message' : 'different user'}, status=401)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

class DeleteCommentView(GenericAPIView):
    serializer_class = CommentSerializer

    @permission_classes(IsAuthenticated, )
    def delete(self, request, gallery_pk, post_pk, comment_pk):
        if request.user.is_authenticated:
            comment = Comment.objects.get(id=comment_pk)

            if comment.user == request.user:
                comment.delete()

                return JsonResponse({'message' : 'Delete success'}, status=200)
            return JsonResponse({'message' : 'Different user'}, status=401)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

# reaction
class LikeView(GenericAPIView):
    serializer_class = LikeSerialzier

    @permission_classes(IsAuthenticated, )
    def post(self, request, gallery_pk, post_pk):
        if request.user.is_authenticated:
            post = Post.objects.get(id=post_pk)

            if post.liked_user.filter(id=request.user.id).exists():
                post.liked_user.remove(request.user)
                message = 'Like Cancle'
            else :
                if post.disliked_user.filter(id=request.user.id).exists():
                    post.disliked_user.remove(request.user)
                post.liked_user.add(request.user)
                message = 'Like'

            like_count = post.liked_user.count()

            return JsonResponse({'message' : message, 'like_count' : like_count}, status=200)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

class DisLikeView(GenericAPIView):
    serializer_class = DisLikeSerializer

    @permission_classes(IsAuthenticated, )
    def post(self, request, gallery_pk, post_pk):
        if request.user.is_authenticated:
            post = Post.objects.get(id=post_pk)

            if post.disliked_user.filter(id=request.user.id).exists():
                post.disliked_user.remove(request.user)
                message = 'DisLike Cancle'
            else :
                if post.liked_user.filter(id=request.user.id).exists():
                    post.liked_user.remove(request.user)
                post.disliked_user.add(request.user)
                message = 'DisLike'

            dislike_count = post.disliked_user.count()

            return JsonResponse({'message' : message, 'dislike_count' : dislike_count}, status=200)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)