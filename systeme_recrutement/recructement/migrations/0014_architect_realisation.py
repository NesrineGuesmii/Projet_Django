# Generated by Django 4.2.1 on 2023-06-12 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recructement', '0013_alter_demande_etat_alter_demande_statut'),
    ]

    operations = [
        migrations.CreateModel(
            name='architect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('Photo', models.ImageField(default='avatar.png', upload_to='uploaded_images/')),
                ('numero', models.IntegerField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='realisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('image', models.ImageField(default='icon_about.png', upload_to='uploaded_images/')),
                ('description', models.TextField()),
                ('architect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recructement.architect')),
            ],
        ),
    ]
