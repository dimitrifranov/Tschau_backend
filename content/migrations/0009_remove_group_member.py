# Generated by Django 3.0.5 on 2020-09-01 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_group_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='member',
        ),
    ]
