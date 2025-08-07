#!/usr/bin/env python
"""
Script pour analyser la structure de la base de données existante
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def analyze_database():
    """Analyser toutes les tables de la base de données"""
    print("📊 === ANALYSE DE LA BASE DE DONNÉES ===")
    
    cursor = connection.cursor()
    
    # Obtenir toutes les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'core_%';")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\n🗃️ Table: {table_name}")
        print("=" * 50)
        
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, name, type_name, not_null, default, primary_key = col
            null_str = "NOT NULL" if not_null else "NULL"
            pk_str = "PRIMARY KEY" if primary_key else ""
            default_str = f"DEFAULT {default}" if default else ""
            print(f"  {name:25} {type_name:15} {null_str:8} {default_str:15} {pk_str}")
        
        # Compter les enregistrements
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  📊 Nombre d'enregistrements: {count}")

def test_models_compatibility():
    """Tester la compatibilité des modèles avec la base de données"""
    print("\n🔍 === TEST COMPATIBILITÉ MODÈLES ===")
    
    try:
        from core.models import Patient, RendezVous, Consultation, Facture, Ordonnance
        from core.models_certificates import CertificatMedical
        
        # Test Patient
        print("\n👤 Test Patient:")
        try:
            patient_count = Patient.objects.count()
            print(f"   ✅ {patient_count} patients trouvés")
            if patient_count > 0:
                patient = Patient.objects.first()
                print(f"   Premier: {patient.nom} {patient.prenom} (CIN: {patient.cin})")
        except Exception as e:
            print(f"   ❌ Erreur Patient: {e}")
        
        # Test RendezVous
        print("\n📅 Test RendezVous:")
        try:
            rdv_count = RendezVous.objects.count()
            print(f"   ✅ {rdv_count} RDV trouvés")
            if rdv_count > 0:
                rdv = RendezVous.objects.first()
                print(f"   Premier: {rdv.patient} - {rdv.date_heure}")
        except Exception as e:
            print(f"   ❌ Erreur RendezVous: {e}")
        
        # Test Consultation
        print("\n🩺 Test Consultation:")
        try:
            consultation_count = Consultation.objects.count()
            print(f"   ✅ {consultation_count} consultations trouvées")
        except Exception as e:
            print(f"   ❌ Erreur Consultation: {e}")
        
        # Test Facture
        print("\n💰 Test Facture:")
        try:
            facture_count = Facture.objects.count()
            print(f"   ✅ {facture_count} factures trouvées")
        except Exception as e:
            print(f"   ❌ Erreur Facture: {e}")
        
        # Test Ordonnance
        print("\n📝 Test Ordonnance:")
        try:
            ordonnance_count = Ordonnance.objects.count()
            print(f"   ✅ {ordonnance_count} ordonnances trouvées")
        except Exception as e:
            print(f"   ❌ Erreur Ordonnance: {e}")
        
        # Test CertificatMedical
        print("\n📄 Test CertificatMedical:")
        try:
            cert_count = CertificatMedical.objects.count()
            print(f"   ✅ {cert_count} certificats trouvés")
            if cert_count > 0:
                cert = CertificatMedical.objects.first()
                print(f"   Premier: {cert.numero_certificat} - {cert.patient}")
        except Exception as e:
            print(f"   ❌ Erreur CertificatMedical: {e}")
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

def show_sample_data():
    """Afficher des échantillons de données"""
    print("\n📋 === ÉCHANTILLONS DE DONNÉES ===")
    
    try:
        from core.models import Patient, RendezVous
        
        # Échantillon de patients
        print("\n👥 Échantillons de patients:")
        patients = Patient.objects.all()[:3]
        for patient in patients:
            print(f"   - {patient.prenom} {patient.nom} ({patient.sexe}, {patient.age} ans)")
        
        # Échantillon de RDV
        print("\n📅 Échantillons de RDV:")
        rdvs = RendezVous.objects.all()[:3]
        for rdv in rdvs:
            print(f"   - {rdv.date_heure.strftime('%d/%m/%Y %H:%M')} - {rdv.patient} - {rdv.statut}")
        
        # Statistiques des statuts RDV
        print("\n📊 Statistiques des statuts RDV:")
        from django.db.models import Count
        statuts = RendezVous.objects.values('statut').annotate(
            nombre=Count('id')
        ).order_by('-nombre')
        
        total_rdv = RendezVous.objects.count()
        for statut in statuts:
            pourcentage = (statut['nombre'] / total_rdv) * 100
            print(f"   - {statut['statut']}: {statut['nombre']} ({pourcentage:.1f}%)")
            
    except Exception as e:
        print(f"❌ Erreur échantillons: {e}")

def main():
    """Fonction principale"""
    print("🔎 === ANALYSE COMPLÈTE DE LA BASE DE DONNÉES ===")
    print(f"Date/heure: {django.utils.timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    try:
        # Analyser la structure
        analyze_database()
        
        # Tester la compatibilité
        test_models_compatibility()
        
        # Afficher des échantillons
        show_sample_data()
        
        print("\n✅ === ANALYSE TERMINÉE ===")
        
    except Exception as e:
        print(f"\n❌ === ERREUR CRITIQUE ===")
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
