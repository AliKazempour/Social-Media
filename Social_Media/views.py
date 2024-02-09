from django.http import Http404
from django.shortcuts import render
from .models import User, Post, Comment, Like, Follower, SavedPost
from .serializers import (
    PostSerializer,
    PostRetrieveUpdateDestroySerializer,
    CommentSerializer,
    CommentRetrieveUpdateDestroySerializer,
    SavedPostSerializer,
    SavedPostRetrieveDestroySerializer,
    UserSerializer
)
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from .permissions import PostUserEditPermission


class ListCreateUser(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        """
        Return a queryset containing all User objects.
        """
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListCreatePostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return the queryset for all Post objects.
        """
        return Post.objects.all()


class RetrieveUpdateDestroyPostView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostRetrieveUpdateDestroySerializer
    permission_classes = [IsAuthenticated, PostUserEditPermission]

    def get_object(self):
        """
        Retrieve and return a specific Post instance based on the pk parameter.
        """
        post_id = self.kwargs.get('pk', None)
        return Post.objects.get(id=post_id)


class ListCreateCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return the queryset for all Comment objects.
        """
        post_id = self.kwargs.get('post_id', None)
        return Comment.objects.filter(post=post_id)


class RetrieveUpdateDestroyCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentRetrieveUpdateDestroySerializer

    def get_object(self):
        """
        Retrieve a comment object from the database based on the provided post_id and comment_id.

        Returns:
            Comment: The retrieved Comment object.
        """
        post_id = self.kwargs.get('post_id', None)
        comment_id = self.kwargs.get('pk', None)
        return Comment.objects.get(id=comment_id, post=post_id)


class ListCreateSavedPostView(generics.ListCreateAPIView):
    serializer_class = SavedPostSerializer

    def get_queryset(self):
        """
        Retrieve a queryset of SavedPost objects filtered by the user_id parameter.
        """
        user_id = self.kwargs.get('user_id', None)
        return SavedPost.objects.filter(user=user_id)


class RetrieveUpdateDestroySavedPostView(generics.RetrieveDestroyAPIView):
    serializer_class = SavedPostRetrieveDestroySerializer

    def get_object(self):
        """
        Retrieves a SavedPost object based on the provided user_id and post_id.
        """
        user_id = self.kwargs.get('user_id')
        post_id = self.kwargs.get('pk')
        return SavedPost.objects.get(id=post_id, user=user_id)
