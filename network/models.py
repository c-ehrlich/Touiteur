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


class Conversation(models.Model):
    user_ids = ArrayField(
        models.PositiveIntegerField(),
        size=2,
    )
    last_message_timestamp = models.DateTimeField(
        default=now,
        # blank=True,
    )
    preview_text = models.TextField(
        blank=True,
    )

    class Meta:
        get_latest_by = '-last_message_timestamp'
        ordering = ['-last_message_timestamp']
        verbose_name = 'DM Thread'
        verbose_name_plural = 'DM Threads'

    def __str__(self):
        return f"{self.user_ids[0]}, {self.user_ids[1]} at {self.last_message_timestamp}: {self.preview_text}"


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
    conversation = models.ForeignKey(
        "Conversation",
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
    )

    class Meta:
        get_latest_by = '-timestamp'
        ordering = ['-timestamp']
        verbose_name = 'DM'
        verbose_name_plural = 'DMs'

    def __str__(self):
        dm = (self.text[:50] + '..') if len(self.text) > 50 else self.text
        return f"{self.sender.username} to {self.recipient.username} at {self.timestamp}: {dm}"

    def save(self, *args, **kwargs):
        # TODO: don't change timestamp if only is_read is changed
        print("in custom DM save")
        conversation = Conversation.objects.filter(
            user_ids__contains=[self.sender.id, self.recipient.id]
        ).first()
        if conversation is None:
            print("no conversation existed for these users. let's create one")
            conversation = Conversation.objects.create(
                user_ids=[self.sender.id, self.recipient.id]
            )
        # if the message is just being created now, update the conversation with its timestamp and text preview
        # if the message is being edited (for example is_read), don't update the conversation
        if self.pk is None:
            dt = datetime.datetime.now(timezone.utc)
            conversation.preview_text = self.text
            conversation.last_message_timestamp=dt
            conversation.save()
            self.conversation = conversation
        super(DirectMessage, self).save(*args, **kwargs)


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
        ('_theme_light', 'Light Mode'),
        ('_theme_dark', 'Dark Mode'),
    )

    LANGUAGES = (
        ('en_US', 'English'),
        ('de', 'Deutsch'),
        ('ja', '日本語'),
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
    blocked_users = models.ManyToManyField(
        "User",
        related_name="blocked_by",
        blank=True
    )
    # likes
    liked_posts = models.ManyToManyField(
        "Post",
        related_name="users_who_liked",
        blank=True
    )
    show_liked_posts = models.BooleanField(
        default=True,
        verbose_name="Show Liked Posts"
    )

    mentions_since_last_checked = models.PositiveIntegerField(
        default=0,
        verbose_name="Mentions since last checked"
    )
    DMs_since_last_checked = models.PositiveIntegerField(
        default=0,
        verbose_name="DMs since last checked",
    )

    theme = models.CharField(
        max_length=20,
        choices=THEMES,
        default='_theme_light',
        verbose_name="Theme"
    )

    language = models.CharField(
        max_length=10,
        choices=LANGUAGES,
        default='en_US',
        verbose_name='Language'
    )
    has_completed_onboarding = models.BooleanField(
        default=False,
        verbose_name="Has Completed Initial Onboarding"
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

    objects = CustomUserManager()


class Post(models.Model):
    author = models.ForeignKey(
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
    reply_to = models.ForeignKey(
        "Post",
        related_name="replies",
        on_delete=models.SET_DEFAULT,
        default=None,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="post-images",
        verbose_name="Image",
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
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        post = (self.text[:50] + '..') if len(self.text) > 50 else self.text
        return f"{self.author.username} at {self.timestamp}: {post}"
