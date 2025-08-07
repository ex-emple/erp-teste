#!/usr/bin/env python
"""
Script de démarrage pour Railway
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Point d'entrée pour Railway"""
    
    # Configuration Django pour Railway
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_railway')
    
    try:
        django.setup()
        
        print("🚀 Démarrage de l'ERP Médical sur Railway...")
        
        # Vérifier si c'est le premier déploiement
        from core.models import Patient
        
        # Migration de la base de données
        print("📦 Migration de la base de données...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Collecte des fichiers statiques
        print("📁 Collecte des fichiers statiques...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        # Création de données de test si la base est vide
        if not Patient.objects.exists():
            print("🏥 Création des données de test...")
            create_test_data()
        
        print("✅ Configuration terminée!")
        print("🌐 Application prête sur Railway!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        sys.exit(1)

def create_test_data():
    """Crée des données de test pour la démonstration"""
    from core.models import Patient, Consultation, Ordonnance
    from datetime import date, datetime, timedelta
    
    # Patients de test
    patients_data = [
        {
            "nom": "Dupont", "prenom": "Jean", "date_naissance": date(1980, 5, 15),
            "sexe": "M", "telephone": "0123456789", "email": "jean.dupont@email.com",
            "adresse": "123 Rue de la Santé, Paris", "cin": "AB123456"
        },
        {
            "nom": "Martin", "prenom": "Marie", "date_naissance": date(1992, 8, 22),
            "sexe": "F", "telephone": "0987654321", "email": "marie.martin@email.com",
            "adresse": "456 Avenue Médicale, Lyon", "cin": "CD789012"
        },
        {
            "nom": "Durand", "prenom": "Pierre", "date_naissance": date(1975, 12, 3),
            "sexe": "M", "telephone": "0567891234", "email": "pierre.durand@email.com",
            "adresse": "789 Boulevard de la Clinique, Marseille", "cin": "EF345678"
        }
    ]
    
    for data in patients_data:
        patient, created = Patient.objects.get_or_create(
            cin=data["cin"], 
            defaults=data
        )
        if created:
            print(f"✅ Patient créé: {patient.nom} {patient.prenom}")
            
            # Ajouter une consultation pour chaque patient
            consultation = Consultation.objects.create(
                patient=patient,
                date_consultation=datetime.now().date() - timedelta(days=7),
                symptomes=f"Consultation de contrôle pour {patient.prenom}",
                diagnostic="Bilan de santé général",
                traitement="Recommandations générales"
            )
            
            # Ajouter une ordonnance
            ordonnance = Ordonnance.objects.create(
                patient=patient,
                consultation=consultation,
                date_prescription=datetime.now().date() - timedelta(days=7),
                medicaments="Vitamines D3\n1 comprimé par jour\nDurée: 30 jours"
            )
    
    print("✅ Données de test créées avec succès!")

if __name__ == '__main__':
    main()
