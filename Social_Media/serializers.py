import django.db
import django.urls
from .models import User, Post, Comment, Like, SavedPost
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})
    date_joined = serializers.DateTimeField(read_only=True)
    num_followers = serializers.IntegerField(read_only=True)
    num_following = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        exclude = ('last_login', 'groups', 'user_permissions',
                   'is_staff', 'is_active', 'is_superuser')


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


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"



class FollowSerializer(serializers.Serializer):
    pass