# Generated by Django 3.0.5 on 2020-04-15 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=500, verbose_name='bio')),
                ('birth_date', models.DateField(verbose_name='Birth_date')),
                ('profile_picture', models.ImageField(blank=True, upload_to='static', verbose_name='Profile Pictures')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'userprofile',
                'verbose_name_plural': 'userprofiles',
            },
        ),
    ]
