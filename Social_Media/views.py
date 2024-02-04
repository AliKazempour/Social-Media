from django.shortcuts import render
from .models import User, Post, Comment, Like, Follower, SavedPost
from .serializers import PostSerializer, PostRetrieveUpdateDestroySerializer, CommentSerializer, CommentRetrieveUpdateDestroySerializer
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
