from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import SignUpSerializer, UserProfileSerializer

User = get_user_model()


# Create your views here.
@csrf_exempt
@api_view(["POST"])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def profile(request, nickname):
    user = User.objects.get(nickname=nickname)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)
