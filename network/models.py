from django.contrib.auth.models import AbstractUser
from django.db import models
from sorl.thumbnail import ImageField
from PIL import Image, ImageOps, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class DirectMessage(models.Model):
    # for now there's just a recipient and user field
    # so when the user account gets deleted, the DMs disappear
    # maybe that's not the best way of doing it IRL?
    # if someone deletes their account, you probably still want to be able
    # to see their messages, for example to prove that they
    # were harrasssing you
    # one solution might be to have additonal sender_username and
    # recipient_username fields that get populated on_delete so the
    # evidence of the post remains
    sender = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="sent_DMs",
        verbose_name="Sender",
    )
    recipient = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="received_DMs",
        verbose_name="Recipient",
    )
    text = models.TextField(
        default="",
        max_length=140,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )
    is_read = models.BooleanField(
        default=False
    )

    class Meta:
        get_latest_by = '-timestamp'
        ordering = ['-timestamp']
        verbose_name = 'DM'
        verbose_name_plural = 'DMs'

    def __str__(self):
        dm = (self.text[:50] + '..') if len(self.text) > 50 else self.text
        return f"{self.sender.username} to f{self.recipient.username} at {self.timestamp}: {dm}"


class User(AbstractUser):
    THEMES = (
        ('_theme_light', 'Light Mode'),
        ('_theme_dark', 'Dark Mode'),
    )

    LANGUAGES = (
        ('EN', 'English'),
        ('DE', 'Deutsch'),
        ('JA', '日本語'),
    )

    avatar = models.ImageField(
        # height_field="avatar_height",
        # width_field="avatar_width",
        default="avatars/default/default_avatar.jpg",
        null=True,
        blank=True,
        editable=True,
        verbose_name="Avatar",
        upload_to="avatars",
    )

    displayname = models.TextField(
        default = "",
        max_length = 100
    )
    bio = models.TextField(
        default = f"",
        max_length = 500
    )

    following = models.ManyToManyField(
        "User",
        related_name="followed_by",
        blank=True
    )
    # likes
    liked_posts = models.ManyToManyField(
        "Post",
        related_name="users_who_liked",
        blank=True
    )

    mentions_since_last_checked = models.PositiveIntegerField(
        default = 0,
        verbose_name="Mentions since last checked"
    )

    theme = models.CharField(
        max_length=20,
        choices=THEMES,
        default='_theme_light',
        verbose_name="Theme"
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        default='EN',
        verbose_name='Language'
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
        return self.username


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
        max_length = 140
    )

    mentioned_users = models.ManyToManyField(
        "User",
        related_name="mentions",
        blank=True,
        editable=False
    )

    class Meta:
        get_latest_by = '-timestamp'
        ordering = ['-timestamp']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        post = (self.text[:50] + '..') if len(self.text) > 50 else self.text
        return f"{self.user.username} at {self.timestamp}: {post}"
