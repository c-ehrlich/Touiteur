# Generated by Django 3.2.4 on 2021-08-05 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0035_alter_post_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='author',
        ),
    ]