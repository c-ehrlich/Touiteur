# Generated by Django 3.2.4 on 2021-07-24 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0028_alter_conversation_last_message_timestamp'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversation',
            options={'get_latest_by': '-last_message_timestamp', 'ordering': ['-last_message_timestamp'], 'verbose_name': 'DM Thread', 'verbose_name_plural': 'DM Threads'},
        ),
        migrations.AddField(
            model_name='conversation',
            name='preview_text',
            field=models.TextField(blank=True),
        ),
    ]
