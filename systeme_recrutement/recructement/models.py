import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Offre(models.Model):
    titre = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    competence = models.CharField(max_length=100)
    formation = models.CharField(max_length=100)
    description = models.TextField()
    publication = models.BooleanField(default=False)
    date_limite = models.DateField(default=timezone.now)
    image = models.ImageField(default='icon_about.png',upload_to='uploaded_images/')
    recruteur = models.ForeignKey(User,on_delete=models.CASCADE)

class demande(models.Model):
    nom = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    duree = models.CharField(max_length=100)
    lieu = models.CharField(max_length=100)
    description = models.TextField()
    Etat = models.CharField(max_length=50,default="Traitement")
    client = models.ForeignKey(User,on_delete=models.CASCADE)
    lancer = models.BooleanField(default=False)
    date_publication = models.DateField(default=timezone.now)
    date_limite = models.DateField(default=timezone.now)
    statut =models.CharField(max_length=100,default="nouveau projet")
    rapport = models.TextField(default="En cours")
    cahier_charge=models.FileField(upload_to='cvs',null=True)


class architect(models.Model):
    description = models.TextField()
    Photo = models.ImageField(default='avatar.png',upload_to='uploaded_images/')
    numero= models.IntegerField()
    profile= models.ForeignKey(User,on_delete=models.CASCADE)
    cv_file=models.FileField(upload_to='cvs',null=True)
    verification=models.CharField(max_length=100,default="non")

class realisation(models.Model):
     architect=models.ForeignKey(User,on_delete=models.CASCADE)
     nom = models.CharField(max_length=100)
     genre = models.CharField(max_length=100)
     image = models.ImageField(default='icon_about.png',upload_to='uploaded_images/')
     description = models.TextField()

class decision(models.Model):
    architect=models.ForeignKey(User,on_delete=models.CASCADE)
    decisionA=models.IntegerField()
    decisioncli=models.IntegerField(null=True)
    demade=models.ForeignKey(demande,on_delete=models.CASCADE,default=200)

class projet(models.Model):
    demande=models.ForeignKey(demande,on_delete=models.CASCADE,default=200)
    architecte=models.CharField(max_length=300,null=True)
    date_debut = models.DateField(default=timezone.now)
    date_fin= models.DateField(default=timezone.now)
    statut =models.CharField(max_length=100,default="nouveau projet")
    rapport = models.TextField(default="En cours",null=True)

class etapes(models.Model):
    projet=models.ForeignKey(projet,on_delete=models.CASCADE,default=1000)
    Étape=models.CharField(max_length=500)
    sous_etape=models.CharField(max_length=500,null=True)
    autre=models.CharField(max_length=500,null=True)
    Date_debut = models.DateField(default=timezone.now)
    Date_fin= models.DateField(default=timezone.now)
    Rapport=models.FileField(upload_to='cvs',null=True)






      







