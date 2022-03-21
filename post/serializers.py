from rest_framework import serializers
from .models import Post, Comment, Like, DisLike

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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'post',
            'user',
            'content',
            'created_at',
        )