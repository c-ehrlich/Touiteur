# Generated by Django 3.2.4 on 2021-07-29 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0032_alter_user_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_completed_onboarding',
            field=models.BooleanField(default=False, verbose_name='Has Completed Initial Onboarding'),
        ),
    ]