from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils import timezone

import logging.config
import logging
from gcinside.settings import DEFAULT_LOGGING

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment, Like, DisLike

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logging.config.dictConfig(DEFAULT_LOGGING)
# Create your views here.
# post
class UploadPostView(APIView):
    @swagger_auto_schema(request_body=PostSerializer)
    @permission_classes(IsAuthenticated, )
    def post(self, request):
        if request.user.is_authenticated:
            serializer = PostSerializer(
                data = {
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
            return JsonResponse({'message' : 'Bad request'}, status=400)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

class UpdatePostView(APIView):
    @swagger_auto_schema(request_body=PostSerializer)
    @permission_classes(IsAuthenticated, )
    def put(self, request, pk):
        if request.user.is_authenticated:
            posting = Post.objects.get(id=pk)

            if posting.author == request.user:
                serializer = PostSerializer(
                    posting,
                    data = {
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

class DeletePostView(APIView):
    @swagger_auto_schema(request_body=PostSerializer)
    @permission_classes(IsAuthenticated, )
    def delete(self, request, pk):
        if request.user.is_authenticated:
            posting = Post.objects.get(id=pk)

            if posting.author == request.user:
                posting.delete()

                return JsonResponse({'message' : 'Delete success'}, status=200)
            return JsonResponse({'message' : 'different user'}, status=401)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

# comment
class UploadCommentView(APIView):
    @permission_classes(IsAuthenticated, )
    def post(self, request, pk):
        if request.user.is_authenticated:
            serializer = CommentSerializer(
                data = {
                    'post' : pk,
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

class UpdateCommentView(APIView):
    @permission_classes(IsAuthenticated, )
    def put(self, request, pk, comment_pk):
        if request.user.is_authenticated:
            comment = Comment.objects.get(id=comment_pk)

            if comment.user == request.user:
                serializer = CommentSerializer(
                    comment,
                    data = {
                        'post' : pk,
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

class DeleteCommentView(APIView):
    @permission_classes(IsAuthenticated, )
    def delete(self, request, pk, comment_pk):
        if request.user.is_authenticated:
            comment = Comment.objects.get(id=comment_pk)

            if comment.user == request.user:
                comment.delete()

                return JsonResponse({'message' : 'Delete success'}, status=200)
            return JsonResponse({'message' : 'Different user'}, status=401)
        else :
            return JsonResponse({'message' : 'auth error'}, status=401)

# reaction
class LikeView(APIView):
    @permission_classes(IsAuthenticated, )
    def post(self, request, pk):
        if request.user.is_authenticated:
            post = Post.objects.get(id=pk)

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

class DisLikeView(APIView):
    @permission_classes(IsAuthenticated, )
    def post(self, request, pk):
        if request.user.is_authenticated:
            post = Post.objects.get(id=pk)

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