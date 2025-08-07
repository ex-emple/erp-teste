#!/usr/bin/env python
"""
Script pour vérifier les données de rendez-vous dans la base
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import RendezVous, Patient, Consultation, Facture
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

def main():
    print("=== VÉRIFICATION DES DONNÉES RDV ===")
    
    # Compter tous les RDV
    total_rdv = RendezVous.objects.count()
    print(f"Total RDV dans la base: {total_rdv}")
    
    if total_rdv == 0:
        print("\n⚠️  AUCUN RDV dans la base de données!")
        print("Vous devez ajouter des RDV pour avoir des statistiques réelles.")
        return
    
    # RDV par statut
    print("\n=== RÉPARTITION PAR STATUT (Toute la base) ===")
    statuts = RendezVous.objects.values('statut').annotate(
        nombre=Count('id')
    ).order_by('-nombre')
    
    for statut in statuts:
        pourcentage = (statut['nombre'] / total_rdv) * 100
        print(f"{statut['statut']}: {statut['nombre']} ({pourcentage:.1f}%)")
    
    # RDV du mois en cours
    today = timezone.now().date()
    debut_mois = today.replace(day=1)
    rdv_mois = RendezVous.objects.filter(
        date_heure__date__range=[debut_mois, today]
    )
    
    print(f"\n=== RDV DU MOIS ACTUEL ({debut_mois} à {today}) ===")
    print(f"Total RDV ce mois: {rdv_mois.count()}")
    
    if rdv_mois.count() > 0:
        statuts_mois = rdv_mois.values('statut').annotate(
            nombre=Count('id')
        ).order_by('-nombre')
        
        for statut in statuts_mois:
            pourcentage = (statut['nombre'] / rdv_mois.count()) * 100
            print(f"  {statut['statut']}: {statut['nombre']} ({pourcentage:.1f}%)")
    else:
        print("  Aucun RDV ce mois")
    
    # Autres statistiques
    print(f"\n=== AUTRES STATISTIQUES ===")
    print(f"Total Patients: {Patient.objects.count()}")
    print(f"Total Consultations: {Consultation.objects.count()}")
    print(f"Total Factures: {Facture.objects.count()}")
    
    # Derniers RDV
    print(f"\n=== DERNIERS RDV ===")
    derniers_rdv = RendezVous.objects.order_by('-date_creation')[:5]
    for rdv in derniers_rdv:
        print(f"  {rdv.date_heure.strftime('%d/%m/%Y %H:%M')} - {rdv.patient} - {rdv.statut}")

if __name__ == '__main__':
    main()
