from rest_framework import viewsets # viewset import
from .serializers import PersonSerializer # 생성한 serializer import
from .models import User # Person model import

class PersonViewSet(viewsets.ModelViewSet): # ModelViewSet 활용
	queryset = Person.objects.all()
    serializer_class = PersonSerializer