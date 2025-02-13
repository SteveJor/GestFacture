from django.forms import ModelForm
from .models import Abonnee, Compteur, Releves, Facture
from django import forms

class AbonneeForm(ModelForm):
    class Meta:
        model = Abonnee
        fields = ['nom', 'tel', 'tarif']

class CompteurForm(ModelForm):
    class Meta:
        model = Compteur
        fields = ['abonnee', 'numero_compteur']

class RelevesForm(ModelForm):
    class Meta:
        model = Releves
        fields = ['compteur', 'date_releve', 'index_avant', 'index_actuelle', 'consommation']


class FactureForm(ModelForm):
    class Meta:
        model = Facture
        fields = ['releve', 'date_facture', 'periode', 'date_echeance']
