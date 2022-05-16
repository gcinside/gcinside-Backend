from django.http.response import JsonResponse

import logging.config
import logging
from gcinside.settings.base import DEFAULT_LOGGING

from .serializers import GallerySerializer

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logging.config.dictConfig(DEFAULT_LOGGING)
# Create your views here.
class UploadGalleryView(GenericAPIView):
    serializer_class = GallerySerializer

    @permission_classes(IsAuthenticated, )
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'gallery_name' : openapi.Schema(type=openapi.TYPE_STRING, description='갤러리 이름'),
            }
        ),
        responses={
            200 : openapi.Response('Success'),
            400 : 'Bad Requset',
            401 : 'Authentication Failed',
        }
    )
    def post(self, request):
        if request.user.is_superuser:
            serializer = GallerySerializer(
                data = {
                    'gallery_name' : request.POST['gallery_name'],
                }
            )

            if serializer.is_valid():
                serializer.save()

                logging.info(request.user)
                return JsonResponse({'message' : 'Upload success'}, status=201)
            return JsonResponse({'message' : 'Bad request'}, stauts=400)
        else :
            return JsonResponse({'message' : 'Authentication Failed'}, status=401)