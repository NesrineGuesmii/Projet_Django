# Generated by Django 4.1.7 on 2023-04-03 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recructement', '0004_offre_image_alter_offre_recruteur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offre',
            name='image',
            field=models.ImageField(default='image.png', upload_to='images/'),
        ),
    ]
