#!/usr/bin/env python
"""
Script pour créer des certificats de test
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Patient
from core.models_certificates import CertificatMedical
from django.utils import timezone
from datetime import date

def main():
    print("=== CRÉATION DE CERTIFICATS DE TEST ===")
    
    # Récupérer des patients
    patients = list(Patient.objects.all()[:3])
    if not patients:
        print("❌ Aucun patient trouvé. Créez d'abord des patients.")
        return
    
    certificats_data = [
        {
            'patient': patients[0],
            'type_certificat': 'arret_travail',
            'contenu': 'Je certifie que M./Mme {nom} présente un état de santé incompatible avec le travail pendant une durée de 3 jours.',
            'duree_arret': 3,
        },
        {
            'patient': patients[1] if len(patients) > 1 else patients[0],
            'type_certificat': 'medical',
            'contenu': 'Je certifie avoir examiné M./Mme {nom} et ne relève aucune contre-indication à la pratique du sport.',
            'duree_arret': None,
        },
        {
            'patient': patients[2] if len(patients) > 2 else patients[0],
            'type_certificat': 'invalidite',
            'contenu': 'Je certifie que M./Mme {nom} présente des limitations fonctionnelles nécessitant un aménagement de poste.',
            'duree_arret': None,
        }
    ]
    
    certificats_crees = 0
    for data in certificats_data:
        # Formater le contenu avec le nom du patient
        contenu = data['contenu'].format(nom=f"{data['patient'].prenom} {data['patient'].nom}")
        
        certificat = CertificatMedical.objects.create(
            patient=data['patient'],
            type_certificat=data['type_certificat'],
            contenu=contenu,
            duree_arret=data['duree_arret'],
            date_emission=timezone.now().date()
        )
        
        certificats_crees += 1
        print(f"✅ Certificat créé: {certificat.numero_certificat} - {certificat.patient} - {certificat.get_type_certificat_display()}")
    
    print(f"\n🎉 {certificats_crees} certificats créés avec succès!")
    
    # Afficher les statistiques
    total_certificats = CertificatMedical.objects.count()
    print(f"Total certificats: {total_certificats}")

if __name__ == '__main__':
    main()
