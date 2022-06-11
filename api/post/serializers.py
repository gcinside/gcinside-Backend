from rest_framework import serializers

from .models import Comment, Like, Post


class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = (
            "gallery",
            "author",
            "title",
            "content",
            "image",
            "created_at",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "post",
            "user",
            "content",
            "created_at",
        )


class LikeSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "user",
            "post",
            "type",
        )
