from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail import ImageField, get_thumbnail


class User(AbstractUser):
    avatar = models.ImageField(
        height_field="avatar_height",
        width_field="avatar_width",
        editable=True,
        help_text="Avatar",
        verbose_name="Avatar",
        upload_to="avatars",
        default="avatars/default/default_avatar.png", # OR DEFAULT TO NONE AND MAKE IT CONTEXTUAL IN VIEWS?
    )
    avatar_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="200")
    avatar_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="200")
    following = models.ManyToManyField(
        "User",
        # on_delete=models.CASCADE,
        related_name="followed_by",
        blank=True
    )
    # likes
    liked_posts = models.ManyToManyField(
        "Post",
        related_name="users_who_liked",
        blank=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    # TODO figure out how to make this work
    # def save(self, *args, **kwargs):
    #     if self.avatar:
    #         self.avatar = get_thumbnail(self.avatar, '200x200', quality=80, format='JPEG')
    #     super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"User {self.username}"

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
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str(self):
        return f"Post by {self.user} at {self.timestamp}"
