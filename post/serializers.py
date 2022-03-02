from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = (
            'author',
            'title',
            'content',
            'image',
            'created_at',
        )