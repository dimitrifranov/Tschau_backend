# Generated by Django 3.0.5 on 2020-09-03 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_delete_membership'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='dfranov01@gmail.com', max_length=254, verbose_name='email'),
            preserve_default=False,
        ),
    ]