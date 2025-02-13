from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from Factures.models import Abonnee, Compteur, Releves, Facture

def accueil(request, indice, Info_abonne):
    indice = int(indice)
    abonne = None
    form = AbonneeForm()

    if request.method == 'POST':
        if indice == 3:
            abonne = get_object_or_404(Abonnee, id=Info_abonne)
            form = AbonneeForm(request.POST, instance=abonne)
            if form.is_valid():
                form.save()
                return render(request, 'GestAbonnes/ModifAbonne.html', {'abonne': abonne, 'form': form})
        elif indice == 4:
            form = AbonneeForm(request.POST)
            if form.is_valid():
                form.save()
                abonnes = Abonnee.objects.all()
                return render(request, 'GestAbonnes/ListeAbonnes.html', {'abonnes': abonnes})
    else:
        if indice == 1:
            abonne = get_object_or_404(Abonnee, id=Info_abonne)
            return render(request, 'GestAbonnes/ModifAbonne.html', {'abonne': abonne, 'form': form})
        elif indice == 5:
            abonne = get_object_or_404(Abonnee, id=Info_abonne)
            abonne.delete()

    abonnes = Abonnee.objects.all()
    return render(request, 'GestAbonnes/ListeAbonnes.html', {'abonnes': abonnes})

def GestCompteurs_view(request, indice, Info_compteur):
    indice = int(indice)
    compteur = None
    form = CompteurForm()
    abonnes = Abonnee.objects.all()

    if request.method == 'POST':
        if indice == 3:
            compteur = get_object_or_404(Compteur, id=Info_compteur)
            form = CompteurForm(request.POST, instance=compteur)
            if form.is_valid():
                form.save()
                return render(request, 'GestCompteur/ModifCompteur.html', {'compteur': compteur, 'form': form, 'abonnes': abonnes})
        elif indice == 4:
            form = CompteurForm(request.POST)
            if form.is_valid():
                form.save()
                compteurs = Compteur.objects.all()
                return render(request, 'GestCompteur/ListCompteurs.html', {'compteurs': compteurs, 'abonnes': abonnes})
    else:
        if indice == 1:
            compteur = get_object_or_404(Compteur, id=Info_compteur)
            return render(request, 'GestCompteur/ModifCompteur.html', {'compteur': compteur, 'form': form, 'abonnes': abonnes})
        elif indice == 5:
            compteur = get_object_or_404(Compteur, id=Info_compteur)
            compteur.delete()

    compteurs = Compteur.objects.all()
    return render(request, 'GestCompteur/ListCompteurs.html', {'compteurs': compteurs, 'abonnes': abonnes})

def GestionReleve_view(request, indice, Info_releve):
    indice = int(indice)
    compteurs = Compteur.objects.all()
    form = RelevesForm()
    abonnes = Abonnee.objects.all()
    releve = None

    if request.method == 'POST':
        if indice == 3:
            releve = get_object_or_404(Releves, id=Info_releve)
            form = RelevesForm(request.POST, instance=releve)
            if form.is_valid():
                form.save()
                date_releve_formatted = releve.date_releve.strftime('%Y-%m-%dT%H:%M')
                return render(request, 'GestReleves/ModifierReleve.html', {'releve': releve, 'form': form, 'date_releve_formatted': date_releve_formatted, 'compteurs': compteurs})
        elif indice == 4:
            form = RelevesForm(request.POST)
            if form.is_valid():
                form.save()
                releves = Releves.objects.all()
                return render(request, 'GestReleves/ListReleves.html', {'releves': releves, 'abonnes': abonnes, 'compteurs': compteurs})
    else:
        if indice == 1:
            releve = get_object_or_404(Releves, id=Info_releve)
            date_releve_formatted = releve.date_releve.strftime('%Y-%m-%dT%H:%M')
            return render(request, 'GestReleves/ModifierReleve.html', {'releve': releve, 'form': form, 'abonnes': abonnes, 'date_releve_formatted': date_releve_formatted, 'compteurs': compteurs})
        elif indice == 5:
            releve = get_object_or_404(Releves, id=Info_releve)
            releve.delete()

    releves = Releves.objects.all()
    return render(request, 'GestReleves/ListReleves.html', {'releves': releves, 'compteurs': compteurs})

def GestionFacture_view(request, indice, Info_facture):
    indice = int(indice)
    abonnes = Abonnee.objects.all()
    form = FactureForm()
    factures = Facture.objects.all()
    releves = Releves.objects.all()
    if request.method == 'POST':
        if indice == 3:
            facture = get_object_or_404(Facture, id=Info_facture)
            form = FactureForm(request.POST, instance=facture)
            if form.is_valid():
                form.save()
                date_facture_formatted = facture.date_facture.strftime('%Y-%m-%d')
                date_echeance_formatted = facture.date_echeance.strftime('%Y-%m-%d')
                return render(request, 'GestFactures/ModifierFacture.html', {'releves': releves,'facture': facture, 'form': form, 'date_echeance_formatted': date_echeance_formatted, 'date_facture_formatted': date_facture_formatted, 'abonnes': abonnes})
        elif indice == 4:
            form = FactureForm(request.POST)
            if form.is_valid():
                releve = form.cleaned_data['releve']
                date_facture = form.cleaned_data['date_facture']
                periode = form.cleaned_data['periode']
                date_echeance = form.cleaned_data['date_echeance']
                montant_total=releve.compteur.abonnee.tarif * releve.consommation
                facture = Facture(
                    releve=releve,
                    date_facture=date_facture,
                    periode=periode,
                    montant_total=montant_total,
                    date_echeance=date_echeance
                )
                facture.save()
                factures = Facture.objects.order_by('-id')
                periodes = periodes = list(set(facture.periode for facture in factures))
                listPrixPeriode=[]
                prixTotal=0
                for periode in periodes:
                    for facture in Facture.objects.filter(periode = periode):
                        prixTotal+=prixTotal + facture.montant_total
                    listPrixPeriode.append({"periode":periode, "montant" :prixTotal})
                    prixTotal=0

                return render(request, 'GestFactures/ListFacture.html', {'releves': releves,'periode': listPrixPeriode, 'abonnes': abonnes, 'factures': factures})
    else:
        if indice == 1:
            facture = get_object_or_404(Facture, id=Info_facture)
            date_facture_formatted = facture.date_facture.strftime('%Y-%m-%d')
            date_echeance_formatted = facture.date_echeance.strftime('%Y-%m-%d')
            return render(request, 'GestFactures/ModifierFacture.html', {'releves': releves,'facture': facture, 'form': form, 'date_echeance_formatted': date_echeance_formatted, 'date_facture_formatted': date_facture_formatted, 'abonnes': abonnes})
        elif indice == 5:
            facture = get_object_or_404(Facture, id=Info_facture)
            facture.delete()
        elif indice == 6:
            factures=Facture.objects.all().filter(periode=Info_facture)
            return render(request, 'facture_template.html', {'factures': factures})


    factures_par_periode = Facture.objects.order_by('periode').order_by('-id')
    periodes = list(set(facture.periode for facture in factures.order_by('-id')))
    listPrixPeriode=[]
    prixTotal=0.0
    for periode in periodes:
        # print(Facture.objects.filter(periode = periode))
        prixTotal=0
        for facture in Facture.objects.filter(periode = periode):
            prixTotal=prixTotal + facture.montant_total
        # print(prixTotal)
        listPrixPeriode.append({"periode":periode, "montant" :prixTotal})
    print(listPrixPeriode)

    return render(request, 'GestFactures/ListFacture.html', {'releves': releves,'periode': listPrixPeriode, 'factures': factures_par_periode, 'abonnes': abonnes})
