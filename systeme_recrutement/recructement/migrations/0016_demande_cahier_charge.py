# Generated by Django 4.2.1 on 2023-06-12 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recructement', '0015_architect_cv_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='cahier_charge',
            field=models.FileField(null=True, upload_to='cvs'),
        ),
    ]