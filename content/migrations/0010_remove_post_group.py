# Generated by Django 3.0.5 on 2020-09-01 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_remove_group_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='group',
        ),
    ]
