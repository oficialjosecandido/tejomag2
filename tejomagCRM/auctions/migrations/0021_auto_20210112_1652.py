# Generated by Django 3.1.3 on 2021-01-12 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_auto_20201226_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='prazo',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='terminado',
            field=models.BooleanField(default=False),
        ),
    ]
