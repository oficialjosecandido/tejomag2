# Generated by Django 3.0.7 on 2021-03-27 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0052_increase_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='increase',
            name='likes',
        ),
    ]