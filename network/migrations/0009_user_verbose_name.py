# Generated by Django 3.2.4 on 2021-07-09 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verbose_name',
            field=models.TextField(default='', max_length=100),
        ),
    ]
