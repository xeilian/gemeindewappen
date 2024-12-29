# Generated by Django 5.1.4 on 2024-12-29 23:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Landkreis',
            fields=[
                ('wikidata_id', models.CharField(default='default_value', max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('coordinates', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'landkreise',
            },
        ),
        migrations.CreateModel(
            name='Wappen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bild', models.ImageField(upload_to='wappen/')),
                ('blasonierung', models.TextField()),
                ('koordinaten', models.CharField(blank=True, max_length=100)),
                ('bbox', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tinktur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('farbe', models.CharField(max_length=20)),
                ('textfarbe', models.CharField(default='#FFFFFF', max_length=20)),
                ('wappen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tinkturen', to='gemeindewappen_website.wappen')),
            ],
        ),
    ]
