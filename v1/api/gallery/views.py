from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils import timezone

import logging.config
import logging
from gcinside.settings import DEFAULT_LOGGING

from .serializers import GallerySerializer

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

logging.config.dictConfig(DEFAULT_LOGGING)
# Create your views here.
class UploadGalleryView(GenericAPIView):
    serializer_class = GallerySerializer

    @permission_classes(IsAuthenticated, )
    def post(self, request):
        if request.user.is_superuser:
            serializer = GallerySerializer(
                data = {
                    'gallery_name' : request.POST['gallery_name'],
                }
            )

            if serializer.is_valid():
                serializer.save()

                return JsonResponse({'message' : 'Upload success'}, status=201)
            return JsonResponse({'message' : 'Bad request'}, stauts=400)
        else :
            return JsonResponse({'message' : 'not admin'}, status=401)