#!/usr/bin/env python
import os
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_prod')
django.setup()

# Import des modèles après la configuration Django
from core.models import Patient, Consultation, Ordonnance, CertificatMedical, Facture, RendezVous, Alerte

def create_initial_data():
    """Crée des données initiales pour la production."""
    
    # Vérifier si des données existent déjà
    if Patient.objects.exists():
        print("Des données existent déjà. Arrêt de la création.")
        return
    
    print("Création des données initiales...")
    
    # Créer quelques patients de test
    patients_data = [
        {
            'nom': 'Dupont',
            'prenom': 'Jean',
            'date_naissance': '1980-05-15',
            'sexe': 'M',
            'telephone': '+33123456789',
            'email': 'jean.dupont@email.com',
            'adresse': '123 Rue de la Santé, Paris',
            'cin': 'AB123456'
        },
        {
            'nom': 'Martin',
            'prenom': 'Marie',
            'date_naissance': '1992-08-22',
            'sexe': 'F',
            'telephone': '+33987654321',
            'email': 'marie.martin@email.com',
            'adresse': '456 Avenue de la Médecine, Lyon',
            'cin': 'CD789012'
        }
    ]
    
    for patient_data in patients_data:
        patient = Patient.objects.create(**patient_data)
        print(f"Patient créé: {patient.nom} {patient.prenom}")
    
    print("Données initiales créées avec succès!")

if __name__ == '__main__':
    create_initial_data()
