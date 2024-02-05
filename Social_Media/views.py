from django.http import Http404
from django.shortcuts import render
from .models import User, Post, Comment, Like, Follower, SavedPost
from .serializers import PostSerializer, PostRetrieveUpdateDestroySerializer, CommentSerializer, CommentRetrieveUpdateDestroySerializer, SavedPostSerializer, SavedPostRetrieveDestroySerializer
from rest_framework import generics


class ListCreatePostView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        Return the queryset for all Post objects.
        """
        return Post.objects.all()


class RetrieveUpdateDestroyPostView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostRetrieveUpdateDestroySerializer

    def get_object(self):
        """
        Retrieve and return a specific Post instance based on the pk parameter.
        """
        post_id = self.kwargs.get('pk', None)
        return Post.objects.get(id=post_id)


class ListCreateCommentView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

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
