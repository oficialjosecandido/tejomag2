# Generated by Django 3.0.7 on 2021-03-08 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0050_auto_20210308_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decrease',
            name='imagem4',
        ),
        migrations.RemoveField(
            model_name='decrease',
            name='imagem5',
        ),
        migrations.RemoveField(
            model_name='increase',
            name='imagem4',
        ),
        migrations.RemoveField(
            model_name='increase',
            name='imagem5',
        ),
        migrations.RemoveField(
            model_name='increase',
            name='imagem6',
        ),
    ]
