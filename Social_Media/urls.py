from django.urls import path
from .views import ListCreatePostView, RetrieveUpdateDestroyPostView, ListCreateCommentView, RetrieveUpdateDestroyCommentView
urlpatterns = [
    path('posts/', ListCreatePostView.as_view(), name='posts'),
    path('posts/<int:pk>/', RetrieveUpdateDestroyPostView.as_view(),
         name='post-details'),
    path('posts/<int:post_id>/comments/',
         ListCreateCommentView.as_view(), name='comments'),
    path('posts/<int:post_id>/comments/<int:pk>/',
         RetrieveUpdateDestroyCommentView.as_view(), name='comment-details'),

]
