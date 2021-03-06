# Generated by Django 4.0.1 on 2022-04-16 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0034_article_author_image_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='author_image_link',
            new_name='author_username',
        ),
        migrations.AlterField(
            model_name='article',
            name='excerpt',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='p1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
