# Generated by Django 3.2.4 on 2021-07-23 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0023_directmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='directmessage',
            old_name='recipients',
            new_name='recipient',
        ),
    ]
