# Generated by Django 4.2.1 on 2023-06-12 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recructement', '0014_architect_realisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='architect',
            name='cv_file',
            field=models.FileField(null=True, upload_to='cvs'),
        ),
    ]
