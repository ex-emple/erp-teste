#!/usr/bin/env python
"""
Script de test complet pour vérifier tous les modèles et fonctionnalités
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Patient, RendezVous, Consultation, Facture, Ordonnance
from core.models_certificates import CertificatMedical
from core.utils.kpi_manager import KPIManager
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

def test_models():
    """Test de tous les modèles"""
    print("🧪 === TEST DES MODÈLES ===")
    
    # Test Patient
    print("\n1. 📋 Test Patient")
    patients_count = Patient.objects.count()
    print(f"   Total patients: {patients_count}")
    if patients_count > 0:
        patient = Patient.objects.first()
        print(f"   Premier patient: {patient}")
        print(f"   Sexe: {patient.sexe}")
        print(f"   Âge: {patient.age} ans")
        print(f"   CIN: {patient.cin}")
        print("   ✅ Modèle Patient OK")
    else:
        print("   ❌ Aucun patient trouvé")
    
    # Test RendezVous
    print("\n2. 📅 Test RendezVous")
    rdv_count = RendezVous.objects.count()
    print(f"   Total RDV: {rdv_count}")
    if rdv_count > 0:
        rdv = RendezVous.objects.first()
        print(f"   Premier RDV: {rdv}")
        print(f"   Statut: {rdv.statut}")
        print(f"   Patient: {rdv.patient}")
        print("   ✅ Modèle RendezVous OK")
        
        # Statistiques des statuts
        from django.db.models import Count
        statuts = RendezVous.objects.values('statut').annotate(
            nombre=Count('id')
        ).order_by('-nombre')
        print("   Répartition des statuts:")
        for statut in statuts:
            pourcentage = (statut['nombre'] / rdv_count) * 100
            print(f"     {statut['statut']}: {statut['nombre']} ({pourcentage:.1f}%)")
    else:
        print("   ❌ Aucun RDV trouvé")
    
    # Test Consultation
    print("\n3. 🩺 Test Consultation")
    consultations_count = Consultation.objects.count()
    print(f"   Total consultations: {consultations_count}")
    if consultations_count > 0:
        consultation = Consultation.objects.first()
        print(f"   Première consultation: {consultation}")
        print(f"   Prix: {consultation.prix} MAD")
        print(f"   Diagnostic: {consultation.diagnostic[:50]}...")
        print("   ✅ Modèle Consultation OK")
    else:
        print("   ❌ Aucune consultation trouvée")
    
    # Test Facture
    print("\n4. 💰 Test Facture")
    factures_count = Facture.objects.count()
    print(f"   Total factures: {factures_count}")
    if factures_count > 0:
        facture = Facture.objects.first()
        print(f"   Première facture: {facture}")
        print(f"   Numéro: {facture.numero}")
        print(f"   Montant TTC: {facture.montant_ttc} MAD")
        print(f"   Statut: {facture.statut}")
        print("   ✅ Modèle Facture OK")
    else:
        print("   ❌ Aucune facture trouvée")
    
    # Test Ordonnance
    print("\n5. 📝 Test Ordonnance")
    ordonnances_count = Ordonnance.objects.count()
    print(f"   Total ordonnances: {ordonnances_count}")
    if ordonnances_count > 0:
        ordonnance = Ordonnance.objects.first()
        print(f"   Première ordonnance: {ordonnance}")
        print(f"   Contenu: {ordonnance.contenu[:50]}...")
        print("   ✅ Modèle Ordonnance OK")
    else:
        print("   ⚠️ Aucune ordonnance trouvée")
    
    # Test CertificatMedical
    print("\n6. 📄 Test CertificatMedical")
    certificats_count = CertificatMedical.objects.count()
    print(f"   Total certificats: {certificats_count}")
    if certificats_count > 0:
        certificat = CertificatMedical.objects.first()
        print(f"   Premier certificat: {certificat}")
        print(f"   Numéro: {certificat.numero_certificat}")
        print(f"   Type: {certificat.get_type_certificat_display()}")
        print(f"   Patient: {certificat.patient}")
        print(f"   Diagnostic: {certificat.diagnostic[:50]}...")
        print("   ✅ Modèle CertificatMedical OK")
    else:
        print("   ⚠️ Aucun certificat trouvé")

def test_kpi_manager():
    """Test du gestionnaire KPI"""
    print("\n🎯 === TEST KPI MANAGER ===")
    
    try:
        # Période de test
        date_fin = timezone.now().date()
        date_debut = date_fin - timedelta(days=30)
        
        print(f"   Période de test: {date_debut} à {date_fin}")
        
        # Test revenus
        revenus = KPIManager.get_revenus_periode(date_debut, date_fin)
        print(f"   💰 Revenus période: {revenus} MAD")
        
        # Test consultations
        consultations = KPIManager.get_consultations_periode(date_debut, date_fin)
        print(f"   🩺 Consultations période: {consultations}")
        
        # Test nouveaux patients
        nouveaux_patients = KPIManager.get_nouveaux_patients_periode(date_debut, date_fin)
        print(f"   👥 Nouveaux patients: {nouveaux_patients}")
        
        # Test certificats
        try:
            certificats = KPIManager.get_certificats_emis_periode(date_debut, date_fin)
            print(f"   📄 Certificats émis: {certificats}")
        except Exception as e:
            print(f"   ⚠️ Erreur certificats: {e}")
        
        # Test top patients
        top_patients = KPIManager.get_top_patients_periode(date_debut, date_fin, 5)
        print(f"   🏆 Top 5 patients:")
        for patient_data in top_patients:
            print(f"     - {patient_data['patient__nom']} {patient_data['patient__prenom']}: {patient_data['nombre']} consultations")
        
        print("   ✅ KPIManager OK")
        
    except Exception as e:
        print(f"   ❌ Erreur KPIManager: {e}")

def test_urls_and_views():
    """Test basique des URLs et vues"""
    print("\n🌐 === TEST URLS ET VUES ===")
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Test URLs de base
        urls_to_test = [
            ('dashboard', 'Dashboard'),
            ('liste_patients', 'Liste patients'),
            ('liste_rdv', 'Liste RDV'),
            ('liste_consultations', 'Liste consultations'),
            ('liste_factures', 'Liste factures'),
            ('dashboard_kpi', 'Dashboard KPI'),
            ('liste_certificats', 'Liste certificats'),
        ]
        
        for url_name, description in urls_to_test:
            try:
                url = reverse(url_name)
                response = client.get(url)
                if response.status_code in [200, 302]:
                    print(f"   ✅ {description}: {response.status_code}")
                else:
                    print(f"   ❌ {description}: {response.status_code}")
            except Exception as e:
                print(f"   ❌ {description}: Erreur - {e}")
                
    except Exception as e:
        print(f"   ❌ Erreur test URLs: {e}")

def test_database_integrity():
    """Test de l'intégrité de la base de données"""
    print("\n🔍 === TEST INTÉGRITÉ BASE DE DONNÉES ===")
    
    try:
        # Test relations
        print("   Test des relations:")
        
        # RDV -> Patient
        rdv_avec_patient = RendezVous.objects.filter(patient__isnull=False).count()
        total_rdv = RendezVous.objects.count()
        print(f"   📅 RDV avec patient: {rdv_avec_patient}/{total_rdv}")
        
        # Consultations -> Patient
        consultations_avec_patient = Consultation.objects.filter(patient__isnull=False).count()
        total_consultations = Consultation.objects.count()
        print(f"   🩺 Consultations avec patient: {consultations_avec_patient}/{total_consultations}")
        
        # Factures -> Patient
        factures_avec_patient = Facture.objects.filter(patient__isnull=False).count()
        total_factures = Facture.objects.count()
        print(f"   💰 Factures avec patient: {factures_avec_patient}/{total_factures}")
        
        # Certificats -> Patient
        certificats_avec_patient = CertificatMedical.objects.filter(patient__isnull=False).count()
        total_certificats = CertificatMedical.objects.count()
        print(f"   📄 Certificats avec patient: {certificats_avec_patient}/{total_certificats}")
        
        # Test données incohérentes
        print("\n   Test cohérence des données:")
        
        # RDV futurs avec statut terminé
        rdv_futurs_termines = RendezVous.objects.filter(
            date_heure__gt=timezone.now(),
            statut='termine'
        ).count()
        if rdv_futurs_termines > 0:
            print(f"   ⚠️ RDV futurs marqués terminés: {rdv_futurs_termines}")
        else:
            print(f"   ✅ Aucun RDV futur marqué terminé")
        
        # Factures avec montant négatif
        factures_negatives = Facture.objects.filter(montant_ttc__lt=0).count()
        if factures_negatives > 0:
            print(f"   ⚠️ Factures avec montant négatif: {factures_negatives}")
        else:
            print(f"   ✅ Aucune facture avec montant négatif")
        
        print("   ✅ Test intégrité terminé")
        
    except Exception as e:
        print(f"   ❌ Erreur test intégrité: {e}")

def create_sample_data():
    """Créer des données d'exemple si nécessaire"""
    print("\n🏗️ === CRÉATION DONNÉES D'EXEMPLE ===")
    
    # Vérifier s'il faut créer des données
    if Ordonnance.objects.count() == 0:
        print("   Création d'ordonnances d'exemple...")
        patients = Patient.objects.all()[:3]
        for i, patient in enumerate(patients):
            Ordonnance.objects.create(
                patient=patient,
                contenu=f"Ordonnance d'exemple {i+1} pour {patient}",
                instructions="À prendre selon les indications médicales"
            )
        print(f"   ✅ {len(patients)} ordonnances créées")
    
    if CertificatMedical.objects.count() < 3:
        print("   Création de certificats d'exemple...")
        patients = Patient.objects.all()[:3]
        types_certificats = ['medical', 'arret_travail', 'sport']
        
        for i, patient in enumerate(patients):
            if i < len(types_certificats):
                CertificatMedical.objects.get_or_create(
                    patient=patient,
                    type_certificat=types_certificats[i],
                    defaults={
                        'diagnostic': f"Diagnostic d'exemple pour {patient}",
                        'description': f"Description du certificat {types_certificats[i]}",
                        'restrictions': "Restrictions selon l'état de santé",
                        'date_emission': timezone.now().date(),
                        'date_debut': timezone.now().date()
                    }
                )
        print(f"   ✅ Certificats vérifiés/créés")

def main():
    """Fonction principale de test"""
    print("🚀 === DÉBUT DES TESTS COMPLETS ===")
    print(f"Date/heure: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Créer des données d'exemple si nécessaire
        create_sample_data()
        
        # Tests des modèles
        test_models()
        
        # Tests KPI
        test_kpi_manager()
        
        # Tests intégrité
        test_database_integrity()
        
        # Tests URLs/Vues
        test_urls_and_views()
        
        print("\n🎉 === TESTS TERMINÉS ===")
        print("✅ Tous les tests ont été exécutés")
        
    except Exception as e:
        print(f"\n❌ === ERREUR CRITIQUE ===")
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
