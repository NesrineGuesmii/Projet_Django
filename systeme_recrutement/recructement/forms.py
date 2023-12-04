from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Offre,demande,decision,projet,architect,realisation,etapes

class UserForm(UserCreationForm):
    ROLE_CHOICES = (
        ('admin', 'Achitecte'),
        ('user', 'client'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rôle')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role'


        ]

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if self.cleaned_data['role'] == 'admin':
            user.is_superuser = True
        if commit:
            user.save()
        return user



class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['titre', 'experience', 'competence', 'formation', 'description','image','publication','date_limite']


class DemandeForm(forms.ModelForm):
     GENRE_CHOICES = (
        ('Extension', 'Extension'),
        ('construction neuve', 'construction neuve'),
        ('Rénovation','Rénovation'),
        ('Aménagement intérieur','Aménagement intérieur'),
        ('Aménagement extérieur','Aménagement extérieur'),
        ('Surélévation','Surélévation')
    )

     genre= forms.ChoiceField(choices=GENRE_CHOICES, label='genre')

     class Meta:
        model = demande
        fields = ['nom', 'genre', 'duree', 'lieu', 'description','date_publication','date_limite','cahier_charge']


class DemandegererForm(forms.ModelForm):
     STATUT_CHOICES = (
        ('En cours', 'En cours'),
        ('suspendu', 'suspendu'),
        ('Livré','Livré')
        
    )

     statut= forms.ChoiceField(choices=STATUT_CHOICES, label='statut')

     class Meta:
        model = projet
        fields = ['date_debut','date_fin','statut','rapport']

class decisionForm(forms.ModelForm):
    class Meta:
        model = decision
        fields = ['architect','decisionA','demade']




class AForm(forms.ModelForm):
    class Meta:
        model = architect
        fields = ['description','Photo','numero','cv_file']


class RForm(forms.ModelForm):
    class Meta:
        model = realisation
        fields = ['nom','genre','image','description']



class etapesForm(forms.ModelForm):


    ETAPES_CHOICES = (
        ('Étape de conception', 'Étape de conception'),
        ('Étape de réalisation', 'Étape de réalisation'),
        ('Étape de suivi de chantier ','Étape de suivi de chantier '),
        ('Étape de réception des travaux ','Étape de réception des travaux ')
        
        )
    
    SSETAPES_CHOICES = (
        ('Étude de faisabilité ', 'Étude de faisabilité'),
        ('Élaboration du programme', 'Élaboration du programme'),
        ('Étude de site  ','Étude de site '),
        ('Conception ','Conception '),
        ('Étude de dimensionnement','Étude de dimensionnement'),
        ('Étude de coût ','Étude de coût '),
        ('Rédaction des plans et devis ','Rédaction des plans et devis'),
        ('Suivi de la construction','Suivi de la construction'),
        ('Réception et exploitation ','Réception et exploitation '),
       
        )
    

    Étape=forms.ChoiceField(choices=ETAPES_CHOICES, label='Étape')
    sous_etape=forms.ChoiceField(choices= SSETAPES_CHOICES, label='sous_etape')
    autre = forms.CharField(required=False)
    class Meta:
        model = etapes
        fields = ['Étape','sous_etape','autre','Date_debut','Date_fin','Rapport']
