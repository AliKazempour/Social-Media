from django.urls import path
from .views import ListCreatePostView,RetrieveUpdateDestroyPostView
urlpatterns = [
    path('posts/', ListCreatePostView.as_view(), name='posts'),
    path('posts/<int:pk>/', RetrieveUpdateDestroyPostView.as_view(), name='post-details'),

]
