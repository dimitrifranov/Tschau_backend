# Generated by Django 3.0.5 on 2020-09-21 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0016_notification_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='actor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='acted_notifs', to=settings.AUTH_USER_MODEL, verbose_name='actors'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_notifs', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
