from django.shortcuts import render, get_object_or_404

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


@api_view(["POST"])
def follow_user(request, nickname):
    if request.user.is_authenticated:
        profile_user = get_object_or_404(User, nickname=nickname)
        login_user = get_object_or_404(User, nickname=request.user.nickname)
        if profile_user == login_user:
            return Response(
                {"message": "나를 팔로우 할 수 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            if login_user in profile_user.followers.all():
                profile_user.followers.remove(login_user)
                return Response(
                    {"message": f"{nickname}님을 팔로우 취소하였습니다."},
                    status=status.HTTP_200_OK,
                )
            else:
                profile_user.followers.add(login_user)
                return Response(
                    {"message": f"{nickname}님을 팔로우하였습니다."},
                    status=status.HTTP_200_OK,
                )
    return Response({"message": "로그인이 필요한 서비스 입니다."})
