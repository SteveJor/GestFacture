from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Abonnee(models.Model):
    nom = models.CharField("Nom Abonnée", max_length=30)
    tel = models.CharField("Téléphone", max_length=30)
    tarif = models.FloatField("Tarif")

    def __str__(self):
        return self.nom

class Compteur(models.Model):
    abonnee = models.ForeignKey(Abonnee, on_delete=models.CASCADE, related_name='compteurs')
    numero_compteur = models.IntegerField("Numéro du compteur")

    def __str__(self):
        return f"Compteur {self.numero_compteur} de {self.abonnee.nom}"

class Releves(models.Model):
    compteur = models.ForeignKey(Compteur, on_delete=models.CASCADE, related_name='releves')
    date_releve = models.DateTimeField("Date relevé")
    index_avant = models.FloatField("Index avant")
    index_actuelle = models.FloatField("Index actuelle")
    consommation = models.FloatField("Consommation", null=True,)

    def __str__(self):
        return f"Relevé du {self.date_releve.strftime('%Y-%m-%d')} pour le compteur {self.compteur.numero_compteur} de {self.compteur.abonnee}"

class Facture(models.Model):
    releve = models.ForeignKey(Releves, on_delete=models.CASCADE, related_name='facture')
    date_facture = models.DateField("Date facture")
    periode = models.CharField("Période", max_length=30)
    montant_total = models.FloatField("Net à payer")
    date_echeance=models.DateField("Date échance")

    def __str__(self):
        return f"Facture du {self.date_facture} {self.periode} pour {self.releve.compteur.abonnee}"
