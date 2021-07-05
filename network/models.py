from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail import ImageField
from PIL import Image, ImageOps, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


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

    def save(self, *args, **kwargs):
        try:
            img = Image.open(self.avatar)
            if img.height > 200 or img.width > 200:
                output_size = (200, 200)
                img = ImageOps.fit(img, output_size, Image.ANTIALIAS)
                img = img.convert('RGB')

                # rotate image correctly based on exif data
                try:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation]=='Orientation':
                            break
                    exif = img.getexif()
                    if exif[orientation] == 3:
                        img = img.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img = img.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img = img.rotate(90, expand=True)
                except (AttributeError, KeyError, IndexError):
                    # cases: image doesn't have getexif
                    pass

                output = BytesIO()
                img.save(output, format='JPEG')
                output.seek(0)
                self.avatar = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f'{self.avatar.name.split(".")[0]}.jpg',
                    'image/jpeg',
                    sys.getsizeof(output),
                    None
                )
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")
        super().save(*args, **kwargs)

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

    def __str__(self):
        post = (self.text[:50] + '..') if len(self.text) > 50 else self.text
        return f"{self.user.username} at {self.timestamp}: {post}"
