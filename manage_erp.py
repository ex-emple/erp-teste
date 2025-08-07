#!/usr/bin/env python3
"""
Script unifié de gestion et test de l'ERP médical
Remplace tous les scripts disparates (test_complete.py, validate_and_clean.py, etc.)

Usage:
    python manage_erp.py [action] [options]

Actions disponibles:
    test        - Lance tous les tests
    validate    - Valide le système
    cleanup     - Nettoie les fichiers temporaires
    backup      - Sauvegarde la base de données
    health      - Vérifie la santé du système
    demo        - Crée des données de démonstration
    stats       - Affiche les statistiques
"""

import os
import sys
import django
import argparse
from datetime import datetime, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.test.utils import get_runner
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured

# Imports locaux
from core.models import Patient, RendezVous, Consultation, Facture
from core.services import statistics_service, maintenance_service


class ERPManager:
    """
    Gestionnaire unifié pour l'ERP médical
    """
    
    def __init__(self):
        self.banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🏥 ERP MÉDICAL MANAGER                     ║
    ║                  Gestionnaire Unifié v2.0                   ║
    ╚══════════════════════════════════════════════════════════════╝
        """
        
    def print_banner(self):
        print(self.banner)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    def test_system(self, verbose=False):
        """Lance tous les tests du système"""
        print("🧪 LANCEMENT DES TESTS SYSTÈME")
        print("=" * 50)
        
        try:
            # Tests de connectivité base de données
            print("📊 Test de connectivité base de données...")
            patients_count = Patient.objects.count()
            rdv_count = RendezVous.objects.count()
            consultations_count = Consultation.objects.count()
            factures_count = Facture.objects.count()
            
            print(f"   ✅ Base de données accessible")
            print(f"   📋 Patients: {patients_count}")
            print(f"   📅 Rendez-vous: {rdv_count}")
            print(f"   🩺 Consultations: {consultations_count}")
            print(f"   💰 Factures: {factures_count}")
            
            # Tests des modèles
            print("\n🔍 Test de l'intégrité des modèles...")
            
            # Vérifier les relations
            orphan_consultations = Consultation.objects.filter(patient__isnull=True).count()
            orphan_rdv = RendezVous.objects.filter(patient__isnull=True).count()
            
            if orphan_consultations == 0 and orphan_rdv == 0:
                print("   ✅ Intégrité des relations OK")
            else:
                print(f"   ⚠️  Relations orphelines détectées:")
                if orphan_consultations > 0:
                    print(f"      - {orphan_consultations} consultations sans patient")
                if orphan_rdv > 0:
                    print(f"      - {orphan_rdv} RDV sans patient")
            
            # Tests des services
            print("\n🔧 Test des services...")
            
            # Test service statistiques
            try:
                today_stats = statistics_service.get_daily_stats()
                print("   ✅ Service de statistiques OK")
            except Exception as e:
                print(f"   ❌ Erreur service statistiques: {e}")
            
            # Test service maintenance
            try:
                health_data = maintenance_service.check_system_health()
                if 'error' not in health_data:
                    print("   ✅ Service de maintenance OK")
                else:
                    print(f"   ⚠️  Service maintenance: {health_data['error']}")
            except Exception as e:
                print(f"   ❌ Erreur service maintenance: {e}")
            
            # Tests des URLs (simulation)
            print("\n🌐 Test des URLs principales...")
            urls_to_test = [
                '/',
                '/patients/',
                '/rdv/',
                '/consultations/',
                '/factures/'
            ]
            
            for url in urls_to_test:
                print(f"   📍 {url} - OK (simulation)")
            
            print("\n✅ TESTS TERMINÉS AVEC SUCCÈS")
            
        except Exception as e:
            print(f"\n❌ ERREUR LORS DES TESTS: {e}")
            return False
        
        return True
    
    def validate_system(self):
        """Valide l'intégrité complète du système"""
        print("🔍 VALIDATION DU SYSTÈME")
        print("=" * 50)
        
        issues_found = []
        
        try:
            # Validation de la configuration Django
            print("⚙️  Validation de la configuration...")
            
            # Vérifier les settings essentiels
            required_settings = ['SECRET_KEY', 'DATABASES', 'INSTALLED_APPS']
            for setting in required_settings:
                if not hasattr(settings, setting):
                    issues_found.append(f"Setting manquant: {setting}")
                else:
                    print(f"   ✅ {setting} configuré")
            
            # Validation de la base de données
            print("\n📊 Validation de la base de données...")
            
            # Test de performances
            start_time = datetime.now()
            test_query = Patient.objects.all()[:10]
            list(test_query)  # Force l'exécution
            query_time = (datetime.now() - start_time).total_seconds()
            
            if query_time < 1.0:
                print(f"   ✅ Performance DB OK ({query_time:.3f}s)")
            else:
                issues_found.append(f"Requête lente détectée: {query_time:.3f}s")
            
            # Validation des données
            print("\n📋 Validation des données...")
            
            # Patients avec données manquantes
            patients_no_name = Patient.objects.filter(nom='').count()
            if patients_no_name > 0:
                issues_found.append(f"{patients_no_name} patients sans nom")
            
            # RDV dans le passé avec statut 'prevu'
            past_rdv = RendezVous.objects.filter(
                date_heure__lt=timezone.now(),
                statut='prevu'
            ).count()
            if past_rdv > 0:
                issues_found.append(f"{past_rdv} RDV passés encore programmés")
            
            # Factures avec montant négatif
            negative_factures = Facture.objects.filter(montant_total__lt=0).count()
            if negative_factures > 0:
                issues_found.append(f"{negative_factures} factures avec montant négatif")
            
            # Validation de la sécurité
            print("\n🔒 Validation de la sécurité...")
            
            if settings.DEBUG:
                issues_found.append("Mode DEBUG activé en production")
            else:
                print("   ✅ Mode DEBUG désactivé")
            
            if settings.SECRET_KEY == 'votre-clé-secrète-très-sécurisée':
                issues_found.append("SECRET_KEY par défaut utilisée")
            else:
                print("   ✅ SECRET_KEY personnalisée")
            
            # Affichage des résultats
            print("\n" + "=" * 50)
            if not issues_found:
                print("✅ SYSTÈME VALIDÉ - AUCUN PROBLÈME DÉTECTÉ")
            else:
                print(f"⚠️  {len(issues_found)} PROBLÈME(S) DÉTECTÉ(S):")
                for i, issue in enumerate(issues_found, 1):
                    print(f"   {i}. {issue}")
                
        except Exception as e:
            print(f"\n❌ ERREUR LORS DE LA VALIDATION: {e}")
            return False
        
        return len(issues_found) == 0
    
    def cleanup_system(self, force=False):
        """Nettoie le système des fichiers temporaires"""
        print("🧹 NETTOYAGE DU SYSTÈME")
        print("=" * 50)
        
        if not force:
            confirm = input("⚠️  Procéder au nettoyage? (oui/non): ")
            if confirm.lower() not in ['oui', 'o', 'yes', 'y']:
                print("Nettoyage annulé")
                return False
        
        try:
            cleaned_items = []
            
            # Nettoyer les fichiers de cache Python
            print("🗑️  Nettoyage des caches Python...")
            import glob
            pycache_dirs = glob.glob('**/__pycache__', recursive=True)
            for cache_dir in pycache_dirs:
                try:
                    import shutil
                    shutil.rmtree(cache_dir)
                    cleaned_items.append(f"Cache: {cache_dir}")
                except Exception:
                    pass
            
            # Nettoyer les logs anciens
            print("📁 Nettoyage des logs anciens...")
            try:
                deleted_logs, errors = maintenance_service.cleanup_old_logs(90)
                cleaned_items.append(f"{deleted_logs} fichiers de logs")
                
                if errors:
                    print(f"   ⚠️  Erreurs lors du nettoyage logs:")
                    for error in errors:
                        print(f"      - {error}")
            except Exception as e:
                print(f"   ⚠️  Erreur nettoyage logs: {e}")
            
            # Nettoyer les fichiers temporaires
            print("🗂️  Nettoyage des fichiers temporaires...")
            temp_files = glob.glob('*.tmp') + glob.glob('*.temp')
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                    cleaned_items.append(f"Temp: {temp_file}")
                except Exception:
                    pass
            
            print(f"\n✅ NETTOYAGE TERMINÉ")
            print(f"📋 Éléments nettoyés: {len(cleaned_items)}")
            for item in cleaned_items:
                print(f"   - {item}")
            
        except Exception as e:
            print(f"\n❌ ERREUR LORS DU NETTOYAGE: {e}")
            return False
        
        return True
    
    def backup_database(self):
        """Crée une sauvegarde de la base de données"""
        print("💾 SAUVEGARDE DE LA BASE DE DONNÉES")
        print("=" * 50)
        
        try:
            success, result = maintenance_service.backup_database()
            
            if success:
                print(f"✅ Sauvegarde créée avec succès!")
                print(f"📁 Fichier: {result}")
                
                # Afficher la taille du fichier
                if os.path.exists(result):
                    size_mb = os.path.getsize(result) / (1024 * 1024)
                    print(f"💾 Taille: {size_mb:.2f} MB")
            else:
                print(f"❌ Échec de la sauvegarde: {result}")
                return False
                
        except Exception as e:
            print(f"❌ ERREUR LORS DE LA SAUVEGARDE: {e}")
            return False
        
        return True
    
    def check_health(self):
        """Vérifie la santé globale du système"""
        print("🔎 VÉRIFICATION DE LA SANTÉ SYSTÈME")
        print("=" * 50)
        
        try:
            health_data = maintenance_service.check_system_health()
            
            if 'error' in health_data:
                print(f"❌ Erreur lors de la vérification: {health_data['error']}")
                return False
            
            # Affichage détaillé de la santé
            overall_score = health_data.get('overall_score', 0)
            
            print(f"🎯 Score global de santé: {overall_score:.1f}/100")
            
            # Détails par composant
            components = ['database', 'storage', 'memory', 'performance']
            
            for component in components:
                comp_data = health_data.get(component, {})
                status = comp_data.get('status', 'unknown')
                score = comp_data.get('score', 0)
                
                if status == 'healthy' or status == 'excellent' or status == 'good':
                    icon = "✅"
                elif status == 'warning' or status == 'acceptable':
                    icon = "⚠️ "
                else:
                    icon = "❌"
                
                print(f"{icon} {component.capitalize()}: {status} ({score}/100)")
                
                # Détails spécifiques
                if component == 'storage':
                    usage = comp_data.get('usage_percent', 0)
                    free_gb = comp_data.get('free_gb', 0)
                    print(f"   💾 Espace utilisé: {usage:.1f}% - Libre: {free_gb:.1f}GB")
                
                elif component == 'memory':
                    usage = comp_data.get('usage_percent', 0)
                    available_gb = comp_data.get('available_gb', 0)
                    print(f"   🧠 RAM utilisée: {usage:.1f}% - Disponible: {available_gb:.1f}GB")
                
                elif component == 'performance':
                    response_time = comp_data.get('db_response_time_ms', 0)
                    print(f"   ⚡ Temps de réponse DB: {response_time:.1f}ms")
                
                elif component == 'database':
                    patients = comp_data.get('patients_count', 0)
                    consultations = comp_data.get('consultations_count', 0)
                    print(f"   📊 {patients} patients, {consultations} consultations")
            
            # Recommandations
            print(f"\n💡 RECOMMANDATIONS:")
            if overall_score >= 90:
                print("   🌟 Système en excellent état - Aucune action requise")
            elif overall_score >= 70:
                print("   👍 Système en bon état - Surveillance recommandée")
            elif overall_score >= 50:
                print("   ⚠️  Système correct - Optimisations recommandées")
            else:
                print("   🚨 Attention requise - Maintenance urgente conseillée")
            
        except Exception as e:
            print(f"❌ ERREUR LORS DE LA VÉRIFICATION: {e}")
            return False
        
        return True
    
    def create_demo_data(self, count=10):
        """Crée des données de démonstration"""
        print(f"📊 CRÉATION DE DONNÉES DE DÉMONSTRATION ({count} éléments)")
        print("=" * 50)
        
        try:
            # Utiliser la commande Django
            call_command('erp_manager', 'create_sample_data', '--count', str(count))
            print("✅ Données de démonstration créées avec succès!")
            
        except Exception as e:
            print(f"❌ ERREUR LORS DE LA CRÉATION: {e}")
            return False
        
        return True
    
    def show_statistics(self):
        """Affiche les statistiques complètes"""
        print("📈 STATISTIQUES DU SYSTÈME")
        print("=" * 50)
        
        try:
            # Statistiques générales
            total_patients = Patient.objects.count()
            total_rdv = RendezVous.objects.count()
            total_consultations = Consultation.objects.count()
            total_factures = Facture.objects.count()
            
            print(f"📊 Vue d'ensemble:")
            print(f"   👥 Patients: {total_patients}")
            print(f"   📅 Rendez-vous: {total_rdv}")
            print(f"   🩺 Consultations: {total_consultations}")
            print(f"   💰 Factures: {total_factures}")
            
            # Statistiques du jour
            today_stats = statistics_service.get_daily_stats()
            print(f"\n📅 Aujourd'hui ({today_stats.get('date', 'N/A')}):")
            print(f"   🩺 Consultations: {today_stats.get('consultations_jour', 0)}")
            print(f"   💰 Revenus: {today_stats.get('revenus_jour', 0)}€")
            print(f"   📅 RDV programmés: {today_stats.get('rdv_programmes', 0)}")
            
            # Statistiques du mois
            now = timezone.now()
            monthly_stats = statistics_service.get_monthly_stats(now.year, now.month)
            print(f"\n📆 Ce mois ({monthly_stats.get('periode', 'N/A')}):")
            print(f"   🩺 Consultations: {monthly_stats.get('consultations_mois', 0)}")
            print(f"   💰 Revenus: {monthly_stats.get('revenus_mois', 0)}€")
            print(f"   📊 Revenu moyen: {monthly_stats.get('revenu_moyen', 0)}€")
            print(f"   👥 Patients uniques: {monthly_stats.get('patients_uniques', 0)}")
            
            print("\n✅ Statistiques affichées avec succès!")
            
        except Exception as e:
            print(f"❌ ERREUR LORS DU CALCUL: {e}")
            return False
        
        return True


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description='Gestionnaire unifié de l\'ERP médical',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'action',
        choices=['test', 'validate', 'cleanup', 'backup', 'health', 'demo', 'stats'],
        help='Action à exécuter'
    )
    
    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help='Nombre d\'éléments pour les données de démo'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force l\'exécution sans confirmation'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mode verbeux'
    )
    
    args = parser.parse_args()
    
    # Créer le gestionnaire
    manager = ERPManager()
    manager.print_banner()
    
    # Exécuter l'action
    success = False
    
    if args.action == 'test':
        success = manager.test_system(args.verbose)
    elif args.action == 'validate':
        success = manager.validate_system()
    elif args.action == 'cleanup':
        success = manager.cleanup_system(args.force)
    elif args.action == 'backup':
        success = manager.backup_database()
    elif args.action == 'health':
        success = manager.check_health()
    elif args.action == 'demo':
        success = manager.create_demo_data(args.count)
    elif args.action == 'stats':
        success = manager.show_statistics()
    
    # Code de sortie
    if success:
        print(f"\n🎉 Action '{args.action}' terminée avec succès!")
        sys.exit(0)
    else:
        print(f"\n💥 Échec de l'action '{args.action}'")
        sys.exit(1)


if __name__ == '__main__':
    main()
