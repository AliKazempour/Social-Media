from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    avatar = models.ImageField(blank=True, null=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    num_followers = models.IntegerField(default=0)
    num_following = models.IntegerField(default=0)
    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False, blank=True, null=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models .ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=20)
    content = models.TextField()
    file = models.FileField(null=True, blank=True, validators=[FileExtensionValidator(
        allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv', 'jpg', 'png'])])
    created = models.DateTimeField(auto_now_add=True)
    num_post_likes = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)


class Comment(models.Model):
    user = models .ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models .ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes')


class SavedPost(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='SavedPosts')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='SavedPosts')
