# Generated by Django 2.2.11 on 2021-01-17 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_auto_20210117_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='/avatars/default.png', upload_to='avatars'),
        ),
    ]
