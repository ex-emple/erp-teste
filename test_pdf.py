#!/usr/bin/env python
"""
Test rapide du téléchargement PDF des certificats
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_pdf_generation():
    """Test de génération PDF"""
    print("🧪 === TEST GÉNÉRATION PDF CERTIFICAT ===")
    
    from core.models_certificates import CertificatMedical
    from django.test import RequestFactory
    from core.views_advanced import generer_certificat_pdf
    
    # Récupérer un certificat
    certificat = CertificatMedical.objects.first()
    if not certificat:
        print("❌ Aucun certificat trouvé pour le test")
        return
    
    print(f"📄 Certificat de test: {certificat}")
    
    # Simuler une requête
    factory = RequestFactory()
    request = factory.get(f'/certificats/{certificat.id}/pdf/')
    
    try:
        # Appeler la vue PDF
        response = generer_certificat_pdf(request, certificat.id)
        
        if response.status_code == 200:
            print("✅ PDF généré avec succès!")
            print(f"   Content-Type: {response.get('Content-Type')}")
            print(f"   Taille: {len(response.content)} bytes")
            
            # Sauvegarder pour test
            with open('test_certificat.pdf', 'wb') as f:
                f.write(response.content)
            print("   📁 PDF sauvegardé: test_certificat.pdf")
            
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()

def show_available_certificates():
    """Afficher les certificats disponibles"""
    print("\n📋 === CERTIFICATS DISPONIBLES ===")
    
    from core.models_certificates import CertificatMedical
    
    certificats = CertificatMedical.objects.all()
    for cert in certificats:
        print(f"   ID: {cert.id} - {cert.numero_certificat} - {cert.patient} - {cert.type_certificat}")

def main():
    """Fonction principale"""
    try:
        from core.models_certificates import CertificatMedical
        
        show_available_certificates()
        test_pdf_generation()
        
        print("\n✅ Test terminé!")
        print("🌐 URL pour tester dans le navigateur:")
        cert = CertificatMedical.objects.first()
        if cert:
            print(f"   http://127.0.0.1:8000/certificats/{cert.id}/pdf/")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
