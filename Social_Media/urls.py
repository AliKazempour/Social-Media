from django.urls import path
from .views import (
    ListCreatePostView,
    RetrieveUpdateDestroyPostView,
    ListCreateCommentView,
    RetrieveUpdateDestroyCommentView,
    ListCreateSavedPostView,
    RetrieveUpdateDestroySavedPostView,
    ListCreateUser,
)
urlpatterns = [
    path('posts/', ListCreatePostView.as_view(), name='posts'),
    path('posts/<int:pk>/', RetrieveUpdateDestroyPostView.as_view(),
         name='post-details'),
    path('posts/<int:post_id>/comments/',
         ListCreateCommentView.as_view(), name='comments'),
    path('posts/<int:post_id>/comments/<int:pk>/',
         RetrieveUpdateDestroyCommentView.as_view(), name='comment-details'),
    path('user/<int:user_id>/savedPosts/',
         ListCreateSavedPostView.as_view(), name='savedPosts'),
    path('user/<int:user_id>/savedPosts/<int:pk>/',
         RetrieveUpdateDestroySavedPostView.as_view(), name='savedPost-details'),
    path('user/', ListCreateUser.as_view(), name='users'),
]
