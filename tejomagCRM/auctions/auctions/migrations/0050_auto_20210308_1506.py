# Generated by Django 3.0.7 on 2021-03-08 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0049_oferta_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decrease',
            name='category',
            field=models.CharField(blank=True, choices=[('Smartphones', 'Smartphones'), ('Computadores', 'Computadores'), ('Tablets', 'Tablets'), ('Consolas', 'Consolas'), ('Televisões', 'Televisões'), ('Drones', 'Drones'), ('Fotografia e Video', 'Fotografia e Video'), ('Outros', 'Outros')], max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='fixed',
            name='category',
            field=models.CharField(blank=True, choices=[('Smartphones', 'Smartphones'), ('Computadores', 'Computadores'), ('Tablets', 'Tablets'), ('Consolas', 'Consolas'), ('Televisões', 'Televisões'), ('Drones', 'Drones'), ('Fotografia e Video', 'Fotografia e Video'), ('Outros', 'Outros')], max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='increase',
            name='category',
            field=models.CharField(blank=True, choices=[('Smartphones', 'Smartphones'), ('Computadores', 'Computadores'), ('Tablets', 'Tablets'), ('Consolas', 'Consolas'), ('Televisões', 'Televisões'), ('Drones', 'Drones'), ('Fotografia e Video', 'Fotografia e Video'), ('Outros', 'Outros')], max_length=64, null=True),
        ),
    ]
