# Generated by Django 4.0.1 on 2022-02-20 16:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_remove_user_nif_user_role_alter_listing_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, max_length=100, unique=True),
        ),
    ]
