# Generated by Django 3.0.5 on 2020-09-22 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_auto_20200922_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='email',
        ),
    ]
