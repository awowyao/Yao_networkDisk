# Generated by Django 4.0.5 on 2023-09-05 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nas', '0002_users_table_user_disk'),
    ]

    operations = [
        migrations.AddField(
            model_name='users_table',
            name='user_disk_size',
            field=models.CharField(default=123, max_length=40),
            preserve_default=False,
        ),
    ]
