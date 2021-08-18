from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import now
from sorl.thumbnail import ImageField
from PIL import Image, ImageOps, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from datetime import timezone
import datetime
from django.templatetags.static import static


from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    """Reduce number of SQL queries 

    This could be expanded by getting a smaller queryset for each
    related prefetch"""
    def get(self, *args, **kwargs):
        return super().prefetch_related(
            'liked_posts',
            'blocked_users',
            'blocked_by'
        ).get(*args, **kwargs)


class User(AbstractUser):
    THEMES = (
        ('_theme_light', _('Light Mode')),
        ('_theme_dark', _('Dark Mode')),
    )

    LANGUAGES = (
        ('en', 'English'),
        ('de', 'Deutsch'),
        ('ja', '日本語'),
    )

    avatar = models.ImageField(
        # height_field="avatar_height",
        # width_field="avatar_width",
        default=static("avatars/default/default_avatar.jpg"),
        null=True,
        blank=True,
        editable=True,
        verbose_name=_("Avatar"),
        upload_to="avatars",
    )

    displayname = models.TextField(
        default = "",
        max_length = 100,
        verbose_name=_("Display Name"),
    )
    bio = models.TextField(
        default = "",
        max_length = 500,
        verbose_name=_("Bio"),
    )
    following = models.ManyToManyField(
        "User",
        related_name="followed_by",
        blank=True,
        verbose_name=_("Following"),
    )
    blocked_users = models.ManyToManyField(
        "User",
        related_name="blocked_by",
        blank=True,
        verbose_name=_("Blocked User"),
    )
    liked_posts = models.ManyToManyField(
        "Post",
        related_name="users_who_liked",
        blank=True,
        verbose_name=_("Liked Post"),
    )
    show_liked_posts = models.BooleanField(
        default=True,
        verbose_name=_("Show Liked Posts"),
    )
    mentions_since_last_checked = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Mentions since last checked"),
    )
    DMs_since_last_checked = models.PositiveIntegerField(
        default=0,
        verbose_name=_("DMs since last checked"),
    )

    theme = models.CharField(
        max_length=20,
        choices=THEMES,
        default='_theme_light',
        verbose_name=_("Theme"),
    )
    language = models.CharField(
        max_length=10,
        choices=LANGUAGES,
        default='en',
        verbose_name=_('Language'),
    )
    has_completed_onboarding = models.BooleanField(
        default=False,
        verbose_name=_("Has Completed Initial Onboarding"),
    )

    class Meta:
        verbose_name = _('User'),
        verbose_name_plural = _('Users'),

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
        return self.username

    objects = CustomUserManager()


class Post(models.Model):
    author = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name=_("Author"),
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Timestamp"),
    )
    text = models.TextField(
        default = "error: post initialized without text",
        max_length = 140,
        verbose_name=_("Text"),
    )
    mentioned_users = models.ManyToManyField(
        "User",
        related_name="mentions",
        blank=True,
        editable=False,
        verbose_name=_("Mentioned User"),
    )
    reply_to = models.ForeignKey(
        "Post",
        related_name="replies",
        on_delete=models.SET_DEFAULT,
        default=None,
        blank=True,
        null=True,
        verbose_name=_("Reply To"),
    )
    image = models.ImageField(
        upload_to="post-images",
        verbose_name=_("Image"),
        default=None,
        blank=True,
        null=True,
        editable=True,
    )
    def save(self, *args, **kwargs):
        try:
            img = Image.open(self.image)
            if img.height > 1024 or img.width > 1024:
                resize_ratio = min(1024/img.height, 1024/img.width)
                output_size = (int(resize_ratio*img.width), int(resize_ratio*img.height))
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
                    f'{self.image.name.split(".")[0]}.jpg',
                    'image/jpeg',
                    sys.getsizeof(output),
                    None
                )
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")
        super().save(*args, **kwargs)

    class Meta:
        get_latest_by = '-timestamp'
        ordering = ['-timestamp']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        post = (self.text[:50] + '..') if len(self.text) > 50 else self.text
        return f"{self.author.username} at {self.timestamp}: {post}"
