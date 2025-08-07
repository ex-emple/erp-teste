#!/usr/bin/env python3
"""
Script pour créer des données de test pour le système ERP médical
"""
import os
import sys
import django
from datetime import datetime, timedelta, time
from decimal import Decimal
import random

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Patient, RendezVous, Consultation
from core.models_certificates import CertificatMedical, RendezVousRecurrent, AlerteRappel

def create_patients():
    """Créer des patients de test"""
    patients_data = [
        {"nom": "Dupont", "prenom": "Jean", "date_naissance": "1980-05-15", "sexe": "M", "telephone": "0101010101", "adresse": "123 Rue de la Paix"},
        {"nom": "Martin", "prenom": "Marie", "date_naissance": "1975-08-22", "sexe": "F", "telephone": "0202020202", "adresse": "456 Avenue Victor Hugo"},
        {"nom": "Bernard", "prenom": "Pierre", "date_naissance": "1990-12-03", "sexe": "M", "telephone": "0303030303", "adresse": "789 Boulevard Saint-Germain"},
        {"nom": "Dubois", "prenom": "Sophie", "date_naissance": "1985-03-17", "sexe": "F", "telephone": "0404040404", "adresse": "321 Rue de Rivoli"},
        {"nom": "Moreau", "prenom": "Luc", "date_naissance": "1970-11-28", "sexe": "M", "telephone": "0505050505", "adresse": "654 Avenue des Champs"},
        {"nom": "Petit", "prenom": "Claire", "date_naissance": "1992-07-09", "sexe": "F", "telephone": "0606060606", "adresse": "987 Rue du Commerce"},
        {"nom": "Durand", "prenom": "Paul", "date_naissance": "1988-01-12", "sexe": "M", "telephone": "0707070707", "adresse": "147 Boulevard Haussmann"},
        {"nom": "Leroy", "prenom": "Anne", "date_naissance": "1983-09-25", "sexe": "F", "telephone": "0808080808", "adresse": "258 Rue Saint-Antoine"},
    ]
    
    patients = []
    for data in patients_data:
        patient, created = Patient.objects.get_or_create(
            nom=data["nom"],
            prenom=data["prenom"],
            defaults=data
        )
        patients.append(patient)
        if created:
            print(f"✓ Patient créé: {patient.nom} {patient.prenom}")
    
    return patients

def create_appointments(patients):
    """Créer des rendez-vous de test"""
    base_date = datetime.now()
    appointments = []
    
    # Rendez-vous passés (pour les KPI)
    for i in range(10):
        date = base_date - timedelta(days=random.randint(1, 30))
        heure = random.choice([8, 9, 10, 11, 14, 15, 16, 17])
        minute = random.choice([0, 15, 30, 45])
        
        date_heure = datetime.combine(date.date(), time(hour=heure, minute=minute))
        
        rdv = RendezVous.objects.create(
            patient=random.choice(patients),
            date_heure=date_heure,
            motif=random.choice([
                "Consultation générale",
                "Contrôle de routine",
                "Suivi médical",
                "Urgence",
                "Vaccination"
            ]),
            statut="termine"
        )
        appointments.append(rdv)
        print(f"✓ RDV créé: {rdv.patient.nom} - {rdv.date_heure.date()}")
    
    # Rendez-vous futurs
    for i in range(15):
        date = base_date + timedelta(days=random.randint(1, 30))
        heure = random.choice([8, 9, 10, 11, 14, 15, 16, 17])
        minute = random.choice([0, 15, 30, 45])
        
        date_heure = datetime.combine(date.date(), time(hour=heure, minute=minute))
        
        rdv = RendezVous.objects.create(
            patient=random.choice(patients),
            date_heure=date_heure,
            motif=random.choice([
                "Consultation générale",
                "Contrôle de routine",
                "Suivi médical",
                "Vaccination",
                "Examen spécialisé"
            ]),
            statut="prevu"
        )
        appointments.append(rdv)
        print(f"✓ RDV futur créé: {rdv.patient.nom} - {rdv.date_heure.date()}")
    
    return appointments

def create_consultations(appointments):
    """Créer des consultations pour les RDV terminés"""
    consultations = []
    
    for rdv in appointments:
        if rdv.statut == "termine":
            consultation = Consultation.objects.create(
                patient=rdv.patient,
                rendez_vous=rdv,
                date_consultation=rdv.date_heure,
                motif=rdv.motif,
                symptomes=random.choice([
                    "Fièvre et maux de tête",
                    "Douleurs articulaires",
                    "Fatigue généralisée",
                    "Toux persistante",
                    "Douleurs abdominales",
                    "Troubles du sommeil",
                    "Aucun symptôme particulier"
                ]),
                examen_clinique=random.choice([
                    "Examen normal",
                    "Tension artérielle élevée",
                    "Température 38.5°C",
                    "Auscultation pulmonaire normale",
                    "Palpation abdominale normale",
                    "Réflexes normaux"
                ]),
                diagnostic=random.choice([
                    "Consultation de routine - RAS",
                    "Grippe saisonnière",
                    "Hypertension artérielle",
                    "Diabète type 2 - suivi",
                    "Allergie pollen",
                    "Lombalgie",
                    "Anxiété",
                    "Consultation préventive"
                ]),
                traitement=random.choice([
                    "Repos et hydratation",
                    "Traitement antihypertenseur",
                    "Antalgiques",
                    "Antihistaminiques",
                    "Kinésithérapie",
                    "Suivi diététique",
                    "Aucun traitement nécessaire"
                ]),
                prix_consultation=Decimal(str(random.randint(50, 150)))
            )
            consultations.append(consultation)
            print(f"✓ Consultation créée: {consultation.patient.nom} - {consultation.prix_consultation} MAD")
    
    return consultations

def create_certificates(consultations):
    """Créer des certificats médicaux"""
    certificates = []
    
    # Créer quelques certificats pour certaines consultations
    selected_consultations = random.sample(consultations, min(5, len(consultations)))
    
    for consultation in selected_consultations:
        duree_arret = random.randint(3, 14)
        date_debut = consultation.date_consultation.date()
        date_fin = date_debut + timedelta(days=duree_arret)
        
        certificat = CertificatMedical.objects.create(
            patient=consultation.patient,
            consultation=consultation,
            type_certificat=random.choice(['arret_travail', 'aptitude', 'repos']),
            date_debut=date_debut,
            date_fin=date_fin,
            duree_arret=duree_arret,
            motif=f"Suite à consultation du {consultation.date_consultation.date()}",
            diagnostic=consultation.diagnostic,
            observations="Repos nécessaire pour récupération complète"
        )
        certificates.append(certificat)
        print(f"✓ Certificat créé: {certificat.numero} - {certificat.patient.nom}")
    
    return certificates

def create_recurring_appointments(patients):
    """Créer des rendez-vous récurrents"""
    recurring = []
    
    # Créer quelques RDV récurrents
    for i in range(3):
        patient = random.choice(patients)
        
        rdv_rec = RendezVousRecurrent.objects.create(
            patient=patient,
            motif=random.choice([
                "Contrôle mensuel diabète",
                "Suivi hypertension",
                "Contrôle cardiologique"
            ]),
            jour_semaine=random.randint(1, 5),  # Lundi à vendredi
            heure=time(
                hour=random.choice([9, 10, 11, 14, 15, 16]),
                minute=random.choice([0, 30])
            ),
            frequence=random.choice(['hebdomadaire', 'mensuelle']),
            date_debut=datetime.now().date(),
            date_fin=datetime.now().date() + timedelta(days=365),
            actif=True
        )
        recurring.append(rdv_rec)
        print(f"✓ RDV récurrent créé: {rdv_rec.patient.nom} - {rdv_rec.frequence}")
    
    return recurring

def create_alerts():
    """Créer des alertes de test"""
    alerts = []
    
    alerts_data = [
        {
            "type_alerte": "rappel",
            "titre": "Rappel vaccination",
            "message": "Rappel de vaccination pour plusieurs patients",
            "priorite": "moyenne",
            "date_echeance": datetime.now().date() + timedelta(days=7)
        },
        {
            "type_alerte": "urgence",
            "titre": "Patient à rappeler",
            "message": "Patient Martin Marie - résultats d'analyse disponibles",
            "priorite": "haute",
            "date_echeance": datetime.now().date() + timedelta(days=1)
        },
        {
            "type_alerte": "certificat",
            "titre": "Certificats expirant",
            "message": "3 certificats médicaux expirent cette semaine",
            "priorite": "moyenne",
            "date_echeance": datetime.now().date() + timedelta(days=3)
        }
    ]
    
    for data in alerts_data:
        alerte = AlerteRappel.objects.create(**data)
        alerts.append(alerte)
        print(f"✓ Alerte créée: {alerte.titre}")
    
    return alerts

def main():
    print("🚀 Création des données de test...")
    print()
    
    # Créer les données
    patients = create_patients()
    print(f"📋 {len(patients)} patients créés\n")
    
    appointments = create_appointments(patients)
    print(f"📅 {len(appointments)} rendez-vous créés\n")
    
    consultations = create_consultations(appointments)
    print(f"🏥 {len(consultations)} consultations créées\n")
    
    certificates = create_certificates(consultations)
    print(f"📋 {len(certificates)} certificats créés\n")
    
    recurring = create_recurring_appointments(patients)
    print(f"🔄 {len(recurring)} RDV récurrents créés\n")
    
    alerts = create_alerts()
    print(f"🔔 {len(alerts)} alertes créées\n")
    
    print("✅ Toutes les données de test ont été créées avec succès!")
    print()
    print("📊 Résumé:")
    print(f"   - Patients: {Patient.objects.count()}")
    print(f"   - Rendez-vous: {RendezVous.objects.count()}")
    print(f"   - Consultations: {Consultation.objects.count()}")
    print(f"   - Certificats: {CertificatMedical.objects.count()}")
    print(f"   - RDV récurrents: {RendezVousRecurrent.objects.count()}")
    print(f"   - Alertes: {AlerteRappel.objects.count()}")

if __name__ == "__main__":
    main()
