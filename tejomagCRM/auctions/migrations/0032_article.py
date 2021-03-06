# Generated by Django 4.0.1 on 2022-04-12 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0031_delete_bid_delete_comment_delete_notification_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('views', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('category', models.CharField(choices=[('Economia', 'Economia'), ('Politica', 'Politica'), ('Mundo', 'Mundo'), ('Desporto', 'Desporto'), ('Justiça', 'Justiça'), ('Lifestyle', 'Lifestyle'), ('Tecnologia', 'Tecnologia'), ('Ciência', 'Ciência')], max_length=64)),
                ('type', models.CharField(choices=[('Entrevista', 'Entrevista'), ('Reportagem', 'Reportagem'), ('Investigação', 'Investigação'), ('Opinião', 'Opinião')], max_length=64)),
                ('title', models.CharField(max_length=30)),
                ('excerpt', models.CharField(max_length=100)),
                ('p1', models.TextField()),
                ('p2', models.TextField(blank=True, null=True)),
                ('p3', models.TextField(blank=True, null=True)),
                ('p4', models.TextField(blank=True, null=True)),
                ('p5', models.TextField(blank=True, null=True)),
                ('image1_link', models.CharField(blank=True, max_length=500, null=True)),
                ('image2_link', models.CharField(blank=True, max_length=500, null=True)),
                ('image3_link', models.CharField(blank=True, max_length=500, null=True)),
                ('image4_link', models.CharField(blank=True, max_length=500, null=True)),
                ('image5_link', models.CharField(blank=True, max_length=500, null=True)),
                ('image6_link', models.CharField(blank=True, max_length=500, null=True)),
                ('image7_link', models.CharField(blank=True, max_length=500, null=True)),
                ('image8_link', models.CharField(blank=True, max_length=500, null=True)),
                ('image9_link', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
