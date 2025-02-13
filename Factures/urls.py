from django.urls import path
from .views import *

urlpatterns = [
    path('Liste des Abonnés/<indice>/<Info_abonne>', accueil, name='accueil'),
    path('Liste des Compteurs/<indice>/<Info_compteur>', GestCompteurs_view, name='GestCompteurs'),
    path('Liste des Relevés/<indice>/<Info_releve>', GestionReleve_view, name='GestionReleve'),
    path('Liste des Factures/<indice>/<Info_facture>', GestionFacture_view, name='GestionFacture'),
]
