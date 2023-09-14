from django.db import models
from teamproject import settings


class Bucket(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # 좋아요
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_buckets', blank=True)
    # 북마크
    bookmarks = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='bookmark_buckets', blank=True)


class Comment(models.Model):
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
