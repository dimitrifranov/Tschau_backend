# Generated by Django 3.0.5 on 2020-09-26 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0025_auto_20200922_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='secret',
            field=models.IntegerField(default=2049575956, editable=False, verbose_name='secret'),
        ),
    ]
