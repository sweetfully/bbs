# Generated by Django 2.2.11 on 2021-01-28 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0006_auto_20210124_1445'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='focus',
            unique_together={('focus_people', 'be_focus_people')},
        ),
    ]
