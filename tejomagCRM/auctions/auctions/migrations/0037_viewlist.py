# Generated by Django 3.1.3 on 2021-02-04 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0036_inverto_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=64)),
                ('listingid', models.IntegerField()),
            ],
        ),
    ]