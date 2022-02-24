from django.contrib import admin
from django.urls import path
from rest_framework import routers
from . import views
router = routers.DefaultRouter()  # DefaultRouter 설정
router.register('person', views.PersonViewSet)  # ViewSet 과 함께 person 이라는 router 등록

urlpatterns = [
    path('', include(router.urls)),
]
