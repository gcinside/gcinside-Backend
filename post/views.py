from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.views import APIView
from .serializers import PostSerializer
import logging.config
import logging
from gcinside.settings import DEFAULT_LOGGING
from django.utils import timezone
from django.contrib.auth import get_user
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

logging.config.dictConfig(DEFAULT_LOGGING)
# Create your views here.
class UploadPostView(APIView):
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

                return JsonResponse({'message' : 'Post success'}, status=201)
            return JsonResponse({'message' : 'Bad request'}, status=400)
        else :
            logging.info(request.user)
            return JsonResponse({'message' : 'auth error'}, status=401)