# Generated by Django 3.1.3 on 2021-01-22 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_auto_20210122_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oferta',
            name='listingid',
            field=models.IntegerField(null=True),
        ),
    ]
