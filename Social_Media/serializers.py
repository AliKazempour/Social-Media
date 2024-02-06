import django.db
from .models import User, Post, Comment, Like, Follower, SavedPost
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})

    class Meta:
        model = User
        exclude = ('last_login', 'groups', 'user_permissions',
                   'is_staff', 'is_active')


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
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "post": {"read_only": True},
        }


class SavedPostSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    # post = serializers.StringRelatedField()
    class Meta:
        model = SavedPost
        fields = "__all__"


class SavedPostRetrieveDestroySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.StringRelatedField()

    class Meta:
        model = SavedPost
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "post": {"read_only": True},
        }
