#!/usr/bin/env python
"""
Test final de toutes les pages du système Mini ERP Docteur
"""

import requests
import sys

def test_url(url, nom_page):
    """Teste une URL et retourne le statut"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ {nom_page} : OK (200)")
            return True
        else:
            print(f"❌ {nom_page} : Erreur {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {nom_page} : Connexion impossible - {e}")
        return False

def main():
    """Test de toutes les pages principales"""
    print("=" * 60)
    print("🧪 TEST DE TOUTES LES PAGES - MINI ERP DOCTEUR")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    pages_a_tester = [
        ("/", "Dashboard Principal"),
        ("/patients/", "Liste des Patients"),
        ("/rdv/", "Liste des RDV"),
        ("/consultations/", "Liste des Consultations"),
        ("/factures/", "Liste des Factures"),
        ("/ordonnances/", "Liste des Ordonnances"),
        ("/certificats/", "Liste des Certificats"),
        ("/kpi/", "Dashboard KPI"),
        ("/admin/", "Interface Admin"),
    ]
    
    resultats = []
    
    print("\n📡 Test des pages principales :")
    for url_path, nom in pages_a_tester:
        url_complete = base_url + url_path
        resultat = test_url(url_complete, nom)
        resultats.append((nom, resultat))
    
    # Test des URLs PDF
    print("\n📄 Test des URLs PDF :")
    pdf_urls = [
        ("/certificats/1/pdf/", "PDF Certificat 1"),
        ("/certificats/2/pdf/", "PDF Certificat 2"),
        ("/certificats/3/pdf/", "PDF Certificat 3"),
        ("/certificats/4/pdf/", "PDF Certificat 4"),
    ]
    
    for url_path, nom in pdf_urls:
        url_complete = base_url + url_path
        resultat = test_url(url_complete, nom)
        resultats.append((nom, resultat))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    pages_ok = sum(1 for _, ok in resultats if ok)
    total_pages = len(resultats)
    
    print(f"✅ Pages fonctionnelles : {pages_ok}/{total_pages}")
    
    if pages_ok == total_pages:
        print("🎉 TOUS LES TESTS RÉUSSIS - SYSTÈME COMPLÈTEMENT OPÉRATIONNEL!")
    else:
        print("⚠️  Certaines pages nécessitent des corrections")
        print("\nPages en erreur :")
        for nom, ok in resultats:
            if not ok:
                print(f"   ❌ {nom}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
