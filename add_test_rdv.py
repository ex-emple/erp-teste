#!/usr/bin/env python
"""
Script pour ajouter des RDV de test avec différents statuts
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import RendezVous, Patient
from django.utils import timezone
from datetime import timedelta, time
import random

def main():
    print("=== AJOUT DE RDV DE TEST ===")
    
    # Récupérer quelques patients
    patients = list(Patient.objects.all()[:5])
    if not patients:
        print("❌ Aucun patient trouvé. Créez d'abord des patients.")
        return
    
    # Statuts possibles
    statuts = ['termine', 'annule', 'absent', 'prevu', 'confirme']
    
    # Créer des RDV pour les 7 derniers jours
    today = timezone.now().date()
    
    rdv_crees = 0
    for i in range(7):
        date_rdv = today - timedelta(days=i)
        
        # Créer 2-5 RDV par jour
        nb_rdv_jour = random.randint(2, 5)
        
        for j in range(nb_rdv_jour):
            patient = random.choice(patients)
            heure = time(hour=random.randint(8, 17), minute=random.choice([0, 30]))
            
            # Choisir un statut (plus de terminés pour les jours passés)
            if i > 0:  # Jours passés
                statut = random.choices(
                    ['termine', 'annule', 'absent'],
                    weights=[70, 20, 10]
                )[0]
            else:  # Aujourd'hui
                statut = random.choices(
                    ['termine', 'prevu', 'confirme'],
                    weights=[50, 30, 20]
                )[0]
            
            # Créer le RDV
            rdv = RendezVous.objects.create(
                patient=patient,
                date_heure=timezone.make_aware(
                    timezone.datetime.combine(date_rdv, heure)
                ),
                motif=f"Consultation de suivi",
                statut=statut
            )
            rdv_crees += 1
            print(f"✅ RDV créé: {date_rdv} {heure} - {patient} - {statut}")
    
    print(f"\n🎉 {rdv_crees} RDV créés avec succès!")
    
    # Afficher les nouvelles statistiques
    print(f"\n=== NOUVELLES STATISTIQUES ===")
    total_rdv = RendezVous.objects.count()
    print(f"Total RDV: {total_rdv}")
    
    from django.db.models import Count
    statuts = RendezVous.objects.values('statut').annotate(
        nombre=Count('id')
    ).order_by('-nombre')
    
    for statut in statuts:
        pourcentage = (statut['nombre'] / total_rdv) * 100
        print(f"  {statut['statut']}: {statut['nombre']} ({pourcentage:.1f}%)")

if __name__ == '__main__':
    main()
