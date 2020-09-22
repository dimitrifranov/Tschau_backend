# Generated by Django 3.0.5 on 2020-09-22 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_auto_20200903_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='comments_notifs',
            field=models.BooleanField(default=True, verbose_name='comments notifications'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='follow_post_notifs',
            field=models.BooleanField(default=True, verbose_name='follower post notifications'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='like_notifs',
            field=models.BooleanField(default=True, verbose_name='like notifications'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='new_follow_notifs',
            field=models.BooleanField(default=True, verbose_name='new follower notifications'),
        ),
    ]
