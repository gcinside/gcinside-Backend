from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh_token'])
        data = {'access_token': str(refresh.access_token)}

        return data

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False,  allow_null=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'username',
            'profile_image',
        )