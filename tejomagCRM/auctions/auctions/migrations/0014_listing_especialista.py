# Generated by Django 3.1.3 on 2020-12-14 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_remove_listing_especialista'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='especialista',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]