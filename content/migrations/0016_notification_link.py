# Generated by Django 3.0.5 on 2020-09-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0015_group_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='link',
            field=models.CharField(default='/post/1', max_length=50, verbose_name='link'),
            preserve_default=False,
        ),
    ]