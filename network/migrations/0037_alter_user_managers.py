# Generated by Django 3.2.4 on 2021-08-05 09:50

from django.db import migrations
import network.models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0036_rename_user_post_author'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', network.models.CustomUserManager()),
            ],
        ),
    ]
