# Generated by Django 3.1.3 on 2021-01-29 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0034_auto_20210126_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[('Smartphones', 'Smartphones'), ('Computadores', 'Computadores'), ('Tablets', 'Tablets'), ('Consolas', 'Consolas'), ('Televisões', 'Televisões'), ('Outros', 'Outros')], max_length=64, null=True),
        ),
    ]
