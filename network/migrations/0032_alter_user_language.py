# Generated by Django 3.2.4 on 2021-07-28 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0031_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('en_US', 'English'), ('de', 'Deutsch'), ('ja', '日本語')], default='en_US', max_length=10, verbose_name='Language'),
        ),
    ]
