# Generated by Django 4.2.1 on 2023-07-01 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recructement', '0031_etapes'),
    ]

    operations = [
        migrations.AddField(
            model_name='etapes',
            name='autre',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
