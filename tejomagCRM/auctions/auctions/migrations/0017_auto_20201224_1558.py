# Generated by Django 3.1.3 on 2020-12-24 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='winner',
            name='image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
