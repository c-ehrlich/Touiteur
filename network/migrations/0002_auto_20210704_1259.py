# Generated by Django 3.2.4 on 2021-07-04 12:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='media/images/default/default_avatar.png', height_field='avatar_height', help_text='Avatar', upload_to='uploads/avatars', verbose_name='Avatar', width_field='avatar_width'),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_height',
            field=models.PositiveIntegerField(blank=True, default='200', editable=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_width',
            field=models.PositiveIntegerField(blank=True, default='200', editable=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followed_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField(default='error: post initialized without text', max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'posts',
                'ordering': ['-timestamp'],
                'get_latest_by': '-timestamp',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(related_name='users_who_liked', to='network.Post'),
        ),
    ]
