import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Point d'entrée principal pour Replit"""
    
    # Configuration de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_replit')
    
    try:
        django.setup()
        
        # Migration automatique de la base de données
        print("🔄 Migration de la base de données...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Collecte des fichiers statiques
        print("📦 Collecte des fichiers statiques...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        # Création des données de test si la base est vide
        print("📊 Vérification des données initiales...")
        from core.models import Patient
        if not Patient.objects.exists():
            print("🏥 Création des données de test...")
            execute_from_command_line(['manage.py', 'shell', '-c', '''
from django.contrib.auth.models import User
from core.models import Patient, Consultation, Ordonnance
from datetime import date, datetime
import random

# Créer quelques patients de test
patients_data = [
    {"nom": "Dupont", "prenom": "Jean", "date_naissance": "1980-05-15", "sexe": "M", "telephone": "0123456789", "email": "jean.dupont@email.com", "adresse": "123 Rue de la Santé", "cin": "AB123456"},
    {"nom": "Martin", "prenom": "Marie", "date_naissance": "1992-08-22", "sexe": "F", "telephone": "0987654321", "email": "marie.martin@email.com", "adresse": "456 Avenue Médicale", "cin": "CD789012"},
    {"nom": "Durand", "prenom": "Pierre", "date_naissance": "1975-12-03", "sexe": "M", "telephone": "0567891234", "email": "pierre.durand@email.com", "adresse": "789 Boulevard de la Clinique", "cin": "EF345678"}
]

for data in patients_data:
    patient, created = Patient.objects.get_or_create(cin=data["cin"], defaults=data)
    if created:
        print(f"Patient créé: {patient.nom} {patient.prenom}")

print("✅ Données de test créées avec succès!")
            '''])
        
        print("🚀 Démarrage du serveur Django...")
        print("🌐 Votre application sera accessible via l'URL fournie par Replit")
        
        # Démarrage du serveur
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
