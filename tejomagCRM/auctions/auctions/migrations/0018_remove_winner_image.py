# Generated by Django 3.1.3 on 2020-12-24 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20201224_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='winner',
            name='image',
        ),
    ]
