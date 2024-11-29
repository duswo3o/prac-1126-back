from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Post, Comment

User = get_user_model()


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "nickname"]


class CommentSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = (
            "post",
            "author",
        )


class PostSerializer(ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    like = AuthorSerializer(many=True)
    like_count = serializers.IntegerField(source="like.count", read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
