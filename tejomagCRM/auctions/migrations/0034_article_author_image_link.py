# Generated by Django 4.0.1 on 2022-04-15 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_article_featured_article_sprint'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author_image_link',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
