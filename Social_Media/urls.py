from django.urls import path
from .views import (
    ListCreatePostView,
    RetrieveUpdateDestroyPostView,
    ListCreateCommentView,
    RetrieveUpdateDestroyCommentView,
    ListCreateSavedPostView,
    RetrieveUpdateDestroySavedPostView,
    RegisterUser,
    ListUserView,
    CreateLikeView
    
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

urlpatterns = [
    path('users/', ListUserView.as_view(), name='users'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(),
         name='token_blacklist'),
    path('posts/', ListCreatePostView.as_view(), name='posts'),
    path('posts/<int:pk>/', RetrieveUpdateDestroyPostView.as_view(),
         name='post-details'),
    path('posts/<int:post_id>/likes/',
         CreateLikeView.as_view(), name='add-like'),
    path('posts/<int:post_id>/comments/',
         ListCreateCommentView.as_view(), name='comments'),
    path('posts/<int:post_id>/comments/<int:pk>/',
         RetrieveUpdateDestroyCommentView.as_view(), name='comment-details'),
    path('user/<int:user_id>/savedPosts/',
         ListCreateSavedPostView.as_view(), name='savedPosts'),
    path('user/<int:user_id>/savedPosts/<int:pk>/',
         RetrieveUpdateDestroySavedPostView.as_view(), name='savedPost-details'),
]
