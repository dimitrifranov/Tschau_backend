# Generated by Django 3.0.5 on 2020-09-11 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0014_auto_20200901_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='public',
            field=models.BooleanField(default=True, verbose_name='public'),
            preserve_default=False,
        ),
    ]