from django.http import Http404
from django.shortcuts import render
from .models import User, Post, Comment, Like, SavedPost, Follow
from .serializers import (
    PostSerializer,
    PostRetrieveUpdateDestroySerializer,
    CommentSerializer,
    CommentRetrieveUpdateDestroySerializer,
    SavedPostSerializer,
    SavedPostRetrieveDestroySerializer,
    UserSerializer,
    LikePostSerializer
)
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from .permissions import PostUserEditPermission, CommentUserEditPermission


class RegisterUser(generics.CreateAPIView):
    """
    API view for registering a new user.
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListUserView(generics.ListAPIView):
    """
    A view for listing users.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """
        Get the queryset for listing users.
        """
        return User.objects.all()


class ListCreatePostView(generics.ListCreateAPIView):
    """
    A view for listing and creating posts.
    """
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

    def perform_create(self, serializer):
        """
        Perform the creation of a comment associated with a specific post.

        Parameters:
        - serializer: The serializer object to process the data for creating the comment.
        """
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        user = self.request.data['user']
        user = User.objects.get(id=user)
        post.num_comments += 1
        comment = Comment.objects.create(
            user=user,
            post=post,
            content=self.request.data['content']
        )
        post.save()
        comment.save()


class RetrieveUpdateDestroyCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentRetrieveUpdateDestroySerializer
    permission_classes = [IsAuthenticated, CommentUserEditPermission]

    def get_object(self):
        """
        Retrieve a comment object from the database based on the provided post_id and comment_id.

        Returns:
            Comment: The retrieved Comment object.
        """
        post_id = self.kwargs.get('post_id', None)
        comment_id = self.kwargs.get('pk', None)
        return Comment.objects.get(id=comment_id, post=post_id)

    def destroy(self, request, *args, **kwargs):
        """
        Override the destroy method to decrement the number of comments for the post.
        """
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        comment_id = self.kwargs.get('pk')
        comment = Comment.objects.get(id=comment_id, post=post)
        if comment.post != post:
            raise ValidationError(
                'This comment does not belong to the specified post.')
        post.num_comments -= 1
        post.save()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class ListCreateLikeView(generics.ListCreateAPIView):
    serializer_class = LikePostSerializer

    def get_queryset(self):
        """
        Get the queryset of likes related to a specific post.
        """
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        like_queryset = Like.objects.filter(post=post)
        return like_queryset

    def perform_create(self, serializer):
        """
        Perform the create action for the Like model.

        Checks if the user has already liked the post, if so raises a validation
        error, else creates a new Like instance and updates the number of likes
        for the post.
        """

        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        user = self.request.data['user']
        user = User.objects.get(id=user)
        like_queryset = Like.objects.filter(user=user, post=post)
        if like_queryset.exists():
            raise ValidationError('You have already liked this post')
        else:
            post.num_post_likes += 1
            like = Like.objects.create(user=user, post=post)
            post.save()
            like.save()
