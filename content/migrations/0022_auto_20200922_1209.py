# Generated by Django 3.0.5 on 2020-09-22 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0021_auto_20200922_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='secret',
            field=models.IntegerField(default=69652506200632, editable=False, verbose_name='secret'),
        ),
    ]