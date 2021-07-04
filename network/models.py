from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(
        height_field="avatar_height",
        width_field="avatar_width",
        editable=True,
        help_text="Avatar",
        verbose_name="Avatar",
        upload_to="uploads/avatars",
        default="media/images/default/default_avatar.png", # OR DEFAULT TO NONE AND MAKE IT CONTEXTUAL IN VIEWS?
    )
    avatar_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="200")
    avatar_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="200")
    following = models.ManyToManyField(
        "User",
        # on_delete=models.CASCADE,
        related_name="followed_by"
    )
    # likes
    liked_posts = models.ManyToManyField(
        "Post",
        # on_delete=models.CASCADE,
        related_name="users_who_liked"
    )

    def __str__(self):
        return f"TODO user str"

class Post(models.Model):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="posts"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    text = models.TextField(
        default = "error: post initialized without text",
        max_length = 500
    )
    class Meta:
        get_latest_by = '-timestamp'
        ordering = ['-timestamp']
        verbose_name = 'post'
        verbose_name = 'posts'

    def __str(self):
        return f"TODO post str"
