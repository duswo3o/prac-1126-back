from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


# 포스트 생성
@api_view(["POST"])
def create_post(request):
    if request.user.is_authenticated:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {"message": "로그인이 필요한 서비스입니다"}, status=status.HTTP_401_UNAUTHORIZED
    )


# 포스트 목록 조회
@api_view(["GET"])
def posts_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 포스트 상세 조회
@api_view(["GET"])
def get_post(request, id):
    post = get_object_or_404(Post, id=id)
    serializer = PostSerializer(post)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 포스트 수정
@api_view(["POST"])
def update_post(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        if request.user == post.author:
            serializer = PostSerializer(instance=post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "수정 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"message": "로그인이 필요한 서비스입니다."})


# 포스트 삭제
@api_view(["POST"])
def delete_post(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        if request.user == post.author:
            post.delete()
            return Response(
                {"message": "포스트가 삭제되었습니다"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"message": "삭제 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"message": "로그인이 필요한 서비스입니다"}, status=status.HTTP_400_BAD_REQUEST
    )


# 댓글 생성
@api_view(["POST"])
def create_comment(request, id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        # content = request.POST.get("content")
        # writer = request.user
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {"message": "로그인이 필요한 서비스입니다."}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
def get_comment(request, id):
    post = get_object_or_404(Post, id=id)
    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 댓글 수정
@api_view(["POST"])
def update_comment(request, comment_id):
    user = request.user
    if user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if user == comment.author:
            serializer = CommentSerializer(
                instance=comment, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "수정 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"message": "로그인이 필요한 서비스입니다."})


# 댓글 삭제
@api_view(["POST"])
def delete_comment(request, comment_id):
    user = request.user
    if user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if user == comment.author:
            comment.delete()
            return Response(
                {"message": "댓글이 삭제되었습니다"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"message": "삭제 권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"message": "로그인이 필요한 서비스입니다"}, status=status.HTTP_400_BAD_REQUEST
    )


# 게시글 좋아요
@api_view(["POST"])
def like_post(request, id):
    user = request.user
    if user.is_authenticated:
        post = get_object_or_404(Post, id=id)
        if user in post.like.all():
            post.like.remove(user)
            return Response({"message": "좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            post.like.add(user)
            return Response({"message": "좋아요"}, status=status.HTTP_200_OK)
    return Response(
        {"message": "로그인이 필요한 서비스입니다."}, status=status.HTTP_400_BAD_REQUEST
    )
