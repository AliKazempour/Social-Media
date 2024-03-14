from django.contrib import admin

import django.db
from .models import User, Post, Comment, Like, Follow, SavedPost


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(SavedPost)
