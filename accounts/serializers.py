from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(ModelSerializer):
    confirm_password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "confirm_password",
            "nickname",
        ]
