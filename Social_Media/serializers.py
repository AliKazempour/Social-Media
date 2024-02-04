from .models import User, Post, Comment, Like, Follower, SavedPost
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class PostRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "post": {"read_only": True},
        }
