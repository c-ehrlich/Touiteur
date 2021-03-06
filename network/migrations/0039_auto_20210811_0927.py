# Generated by Django 3.2.4 on 2021-08-11 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0038_alter_user_language'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': ('User',), 'verbose_name_plural': ('Users',)},
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='mentioned_users',
            field=models.ManyToManyField(blank=True, editable=False, related_name='mentions', to=settings.AUTH_USER_MODEL, verbose_name='Mentioned User'),
        ),
        migrations.AlterField(
            model_name='post',
            name='reply_to',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='replies', to='network.post', verbose_name='Reply To'),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(default='error: post initialized without text', max_length=140, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(default='', max_length=500, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='blocked_users',
            field=models.ManyToManyField(blank=True, related_name='blocked_by', to=settings.AUTH_USER_MODEL, verbose_name='Blocked User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='displayname',
            field=models.TextField(default='', max_length=100, verbose_name='Display Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followed_by', to=settings.AUTH_USER_MODEL, verbose_name='Following'),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(blank=True, related_name='users_who_liked', to='network.Post', verbose_name='Liked Post'),
        ),
    ]
