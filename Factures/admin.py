from django.contrib import admin
from .models import Abonnee, Compteur, Releves, Facture

# Enregistrement des modèles dans l'interface d'administration
@admin.register(Abonnee)
class AbonneeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'tel', 'tarif')
    search_fields = ('nom', 'tel')
    list_filter = ('tarif',)

@admin.register(Compteur)
class CompteurAdmin(admin.ModelAdmin):
    list_display = ('numero_compteur', 'abonnee')
    search_fields = ('numero_compteur', 'abonnee__nom')
    list_filter = ('abonnee',)

@admin.register(Releves)
class RelevesAdmin(admin.ModelAdmin):
    list_display = ('compteur', 'date_releve', 'index_avant', 'index_actuelle', 'consommation')
    search_fields = ('compteur__numero_compteur', 'date_releve')
    list_filter = ('compteur__abonnee', 'date_releve')

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ('date_facture', 'periode', 'montant_total')
    search_fields = ('date_facture', 'periode')
    list_filter = ('date_facture', 'periode')
