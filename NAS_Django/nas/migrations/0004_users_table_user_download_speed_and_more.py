# Generated by Django 4.0.5 on 2023-09-16 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nas', '0003_users_table_user_disk_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='users_table',
            name='user_download_speed',
            field=models.IntegerField(default=200),
        ),
        migrations.AddField(
            model_name='users_table',
            name='user_oss_msg',
            field=models.TextField(null=True),
        ),
    ]
