from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class ForumUser(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(default="")
    entry_count = models.IntegerField(verbose_name="entry count", default=0)
    post_count = models.IntegerField(verbose_name="post count", default=0)
    is_elite = models.BooleanField(verbose_name="is elite", default=False)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Post(models.Model):
    author = models.ForeignKey(
        ForumUser,
        on_delete=models.CASCADE,
        verbose_name="related author",
        related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = 'Post'


class Entry(models.Model):
    author = models.ForeignKey(
        ForumUser,
        on_delete=models.CASCADE,
        verbose_name="related author",
        related_name="entries")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="related post",
        related_name="entries"
    )
    content = models.TextField()
    wrote_day = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:20]

    class Meta:
        ordering = ["updated_at"]
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'


