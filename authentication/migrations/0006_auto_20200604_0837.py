# Generated by Django 3.0.5 on 2020-06-04 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_userprofile_signal_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.FileField(blank=True, null=True, upload_to='profile_picture', verbose_name='Profile Pictures'),
        ),
    ]
