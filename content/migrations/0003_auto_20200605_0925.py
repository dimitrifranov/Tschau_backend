# Generated by Django 3.0.5 on 2020-06-05 09:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0002_auto_20200605_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='creator'),
            preserve_default=False,
        ),
    ]
