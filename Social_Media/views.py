from django.shortcuts import render
from .models import User, Post, Comment, Like, Follower, SavedPost
from .serializers import PostSerializer, PostRetrieveUpdateDestroySerializer
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