"""
Script de validation et de nettoyage pour l'application Cabinet Médical
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Configuration pour exécuter Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.exceptions import ValidationError
from core.models import Patient, RendezVous, Consultation, Ordonnance, Facture
from core.models_config import CabinetConfig, NotificationConfig


def valider_donnees():
    """Valide toutes les données de l'application"""
    print("🔍 Validation des données en cours...")
    
    erreurs = []
    
    # Validation des patients
    patients_invalides = []
    for patient in Patient.objects.all():
        try:
            patient.full_clean()
        except ValidationError as e:
            patients_invalides.append(f"Patient {patient.id}: {e}")
    
    if patients_invalides:
        erreurs.extend(patients_invalides)
    
    # Validation des rendez-vous
    rdv_invalides = []
    for rdv in RendezVous.objects.all():
        try:
            rdv.full_clean()
        except ValidationError as e:
            rdv_invalides.append(f"RDV {rdv.id}: {e}")
    
    if rdv_invalides:
        erreurs.extend(rdv_invalides)
    
    # Validation des consultations
    consultations_invalides = []
    for consultation in Consultation.objects.all():
        try:
            consultation.full_clean()
        except ValidationError as e:
            consultations_invalides.append(f"Consultation {consultation.id}: {e}")
    
    if consultations_invalides:
        erreurs.extend(consultations_invalides)
    
    # Validation des factures
    factures_invalides = []
    for facture in Facture.objects.all():
        try:
            facture.full_clean()
        except ValidationError as e:
            factures_invalides.append(f"Facture {facture.id}: {e}")
    
    if factures_invalides:
        erreurs.extend(factures_invalides)
    
    if erreurs:
        print("❌ Erreurs de validation trouvées:")
        for erreur in erreurs:
            print(f"  - {erreur}")
        return False
    else:
        print("✅ Toutes les données sont valides!")
        return True


def verifier_configuration():
    """Vérifie la configuration du cabinet"""
    print("\n🔧 Vérification de la configuration...")
    
    config = CabinetConfig.get_config()
    notification_config = NotificationConfig.get_config()
    
    warnings = []
    
    # Vérification des informations essentielles
    if config.nom_medecin == "Dr. [Votre Nom]":
        warnings.append("Le nom du médecin n'a pas été personnalisé")
    
    if config.telephone == "+212 5XX XXX XXX":
        warnings.append("Le numéro de téléphone n'a pas été personnalisé")
    
    if config.email == "contact@abnclinic.ma":
        warnings.append("L'email n'a pas été personnalisé")
    
    if config.adresse == "123 Avenue Mohammed V, Casablanca, Maroc":
        warnings.append("L'adresse n'a pas été personnalisée")
    
    if warnings:
        print("⚠️  Avertissements de configuration:")
        for warning in warnings:
            print(f"  - {warning}")
        print("💡 Personnalisez la configuration via /admin/ ou la commande init_config")
    else:
        print("✅ Configuration du cabinet complète!")
    
    return len(warnings) == 0


def nettoyer_fichiers_temporaires():
    """Nettoie les fichiers temporaires"""
    print("\n🧹 Nettoyage des fichiers temporaires...")
    
    # Fichiers à nettoyer
    fichiers_temp = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.DS_Store',
        'Thumbs.db'
    ]
    
    import glob
    import shutil
    
    nettoyage_effectue = False
    
    for pattern in fichiers_temp:
        if pattern == '__pycache__':
            # Supprimer les dossiers __pycache__
            for root, dirs, files in os.walk('.'):
                if '__pycache__' in dirs:
                    cache_path = os.path.join(root, '__pycache__')
                    shutil.rmtree(cache_path)
                    print(f"  ✅ Supprimé: {cache_path}")
                    nettoyage_effectue = True
        else:
            # Supprimer les fichiers correspondant au pattern
            files = glob.glob(f"**/{pattern}", recursive=True)
            for file in files:
                try:
                    os.remove(file)
                    print(f"  ✅ Supprimé: {file}")
                    nettoyage_effectue = True
                except OSError:
                    pass
    
    if not nettoyage_effectue:
        print("  ✅ Aucun fichier temporaire à nettoyer")


def verifier_securite():
    """Vérifie les paramètres de sécurité"""
    print("\n🔒 Vérification de la sécurité...")
    
    warnings = []
    
    # Vérifier DEBUG
    if settings.DEBUG:
        warnings.append("DEBUG=True en production est dangereux")
    
    # Vérifier SECRET_KEY
    if settings.SECRET_KEY == 'django-insecure-your-secret-key-here':
        warnings.append("SECRET_KEY par défaut détectée")
    
    # Vérifier ALLOWED_HOSTS
    if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['*']:
        warnings.append("ALLOWED_HOSTS mal configuré")
    
    if warnings:
        print("⚠️  Avertissements de sécurité:")
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("✅ Configuration de sécurité correcte!")
    
    return len(warnings) == 0


def afficher_statistiques():
    """Affiche les statistiques de l'application"""
    print("\n📊 Statistiques de l'application:")
    print(f"  - Patients: {Patient.objects.count()}")
    print(f"  - Rendez-vous: {RendezVous.objects.count()}")
    print(f"  - Consultations: {Consultation.objects.count()}")
    print(f"  - Ordonnances: {Ordonnance.objects.count()}")
    print(f"  - Factures: {Facture.objects.count()}")
    
    # Factures impayées
    factures_impayees = Facture.objects.filter(statut='en_attente').count()
    if factures_impayees > 0:
        print(f"  ⚠️  Factures impayées: {factures_impayees}")
    
    # Revenus du mois
    from django.db.models import Sum
    from django.utils import timezone
    
    today = timezone.now().date()
    revenus_mois = Facture.objects.filter(
        date_facture__month=today.month,
        statut='payee'
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    
    print(f"  💰 Revenus du mois: {revenus_mois} DH")


def main():
    """Fonction principale de validation et nettoyage"""
    print("🏥 Validation et nettoyage de l'application Cabinet Médical")
    print("=" * 60)
    
    # Validation des données
    donnees_valides = valider_donnees()
    
    # Vérification de la configuration
    config_complete = verifier_configuration()
    
    # Nettoyage des fichiers temporaires
    nettoyer_fichiers_temporaires()
    
    # Vérification de la sécurité
    securite_ok = verifier_securite()
    
    # Affichage des statistiques
    afficher_statistiques()
    
    print("\n" + "=" * 60)
    
    if donnees_valides and config_complete and securite_ok:
        print("✅ Application validée et nettoyée avec succès!")
        print("🚀 L'application est prête pour la production.")
    else:
        print("⚠️  Certains problèmes ont été détectés.")
        print("📝 Consultez les messages ci-dessus pour plus de détails.")
    
    print("\n💡 Pour démarrer l'application: python manage.py runserver")


if __name__ == "__main__":
    main()
