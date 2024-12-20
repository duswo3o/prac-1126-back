from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers

from posts.serializers import PostSerializer

User = get_user_model()


class SignUpSerializer(ModelSerializer):
    confirm_password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
            "nickname",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"message": "패스워드가 일치하지 않습니다."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            nickname=validated_data["nickname"],
        )
        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "nickname"]


class UserProfileSerializer(ModelSerializer):
    posts = PostSerializer(read_only=True, many=True)
    followings = UserSerializer(read_only=True, many=True)
    followers = UserSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nickname",
            "bio",
            "gender",
            "posts",
            "followings",
            "followers",
        ]
        # read_only_fields = ("id",)


class EditProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "bio", "gender"]
