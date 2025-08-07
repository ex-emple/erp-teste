# Mini ERP Cabinet Médical

Un système de gestion simple et complet pour cabinet médical au Maroc.

## 🚀 Fonctionnalités

- 📋 **Gestion des patients** - Fiche complète avec antécédents médicaux et allergies
- 📆 **Prise de rendez-vous** - Planification et suivi des rendez-vous
- 🩺 **Consultations** - Enregistrement détaillé des consultations médicales
- 💊 **Ordonnances (PDF)** - Génération automatique d'ordonnances en PDF
- 💰 **Facturation simple** - Gestion des factures et paiements
- 📈 **Statistiques de base** - Tableau de bord avec revenus et statistiques

## 🛠 Installation

### Prérequis
- Python 3.8 ou supérieur
- Git (optionnel)

### Étapes d'installation

1. **Créer un environnement virtuel :**
```bash
python -m venv venv
```

2. **Activer l'environnement virtuel :**
```bash
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

4. **Effectuer les migrations :**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Créer un superutilisateur :**
```bash
python manage.py createsuperuser
```

6. **Initialiser des données de test (optionnel) :**
```bash
python manage.py init_data
```

7. **Lancer le serveur :**
```bash
python manage.py runserver
```

## 🎯 Utilisation

### Accès à l'application
- **Interface principale :** `http://127.0.0.1:8000`
- **Administration Django :** `http://127.0.0.1:8000/admin`

### Première utilisation

1. **Connectez-vous** avec votre compte superutilisateur
2. **Ajoutez des patients** via le menu "Patients"
3. **Planifiez des rendez-vous** via le menu "Rendez-vous"
4. **Enregistrez des consultations** après chaque visite
5. **Générez des ordonnances** en PDF si nécessaire
6. **Gérez la facturation** via le menu "Factures"

## 📊 Fonctionnalités détaillées

### Gestion des patients
- Informations personnelles complètes
- Antécédents médicaux et allergies
- Historique des consultations
- Recherche rapide par nom, téléphone, etc.

### Rendez-vous
- Planification avec date/heure
- Statuts : prévu, confirmé, terminé, annulé
- Vue calendrier des prochains rendez-vous
- Filtrage par date et statut

### Consultations
- Motif de consultation
- Symptômes et examen clinique
- Diagnostic et traitement
- Recommandations
- Lien automatique avec les rendez-vous

### Ordonnances
- Médicaments prescrits avec posologie
- Durée du traitement
- Examens complémentaires
- **Génération automatique en PDF**
- Template personnalisable

### Facturation
- Numérotation automatique des factures
- Gestion des paiements (espèces, chèque, carte, virement)
- Statuts : en attente, payée, partiellement payée
- Frais supplémentaires et réductions
- Calcul automatique des totaux

### Tableau de bord
- Statistiques en temps réel
- Prochains rendez-vous
- Actions rapides
- Alertes (factures impayées, etc.)

## 🔧 Personnalisation

### Informations du cabinet
Modifiez les fichiers suivants pour personnaliser votre cabinet :

1. **Dans les templates d'ordonnances** (`core/utils/pdf.py`) :
   - Nom du médecin
   - Adresse du cabinet
   - Téléphone et email

2. **Dans les paramètres** (`config/settings.py`) :
   - Fuseau horaire (défaut: Africa/Casablanca)
   - Langue (défaut: fr-fr)

### Prix par défaut
Modifiez le prix de consultation par défaut dans `core/models.py` :
```python
prix_consultation = models.DecimalField(..., default=250.00, ...)
```

## 📁 Structure du projet

```
erp_cabinet/
├── manage.py                    # Script de gestion Django
├── requirements.txt             # Dépendances Python
├── README.md                   # Ce fichier
├── .gitignore                  # Fichiers à ignorer par Git
│
├── config/                     # Configuration Django
│   ├── settings.py             # Paramètres de l'application
│   ├── urls.py                 # URLs principales
│   └── wsgi.py                 # Configuration WSGI
│
├── core/                       # Application principale
│   ├── models.py               # Modèles de données
│   ├── views.py                # Logique métier
│   ├── forms.py                # Formulaires
│   ├── urls.py                 # URLs de l'application
│   ├── admin.py                # Interface d'administration
│   ├── templates/core/         # Templates HTML
│   ├── management/commands/    # Commandes personnalisées
│   └── utils/                  # Utilitaires (PDF, etc.)
│
├── static/                     # Fichiers statiques
│   ├── css/                    # Styles CSS
│   └── js/                     # Scripts JavaScript
│
└── db.sqlite3                  # Base de données (créée automatiquement)
```

## 🚨 Important

### Sécurité
- Changez la `SECRET_KEY` en production
- Désactivez `DEBUG = False` en production
- Configurez `ALLOWED_HOSTS` pour votre domaine

### Sauvegarde
- Sauvegardez régulièrement `db.sqlite3`
- Exportez vos données importantes

### Mise à jour
- Toujours tester en environnement de développement
- Effectuer une sauvegarde avant mise à jour

## 🆘 Support

### Problèmes courants

**Erreur de migration :**
```bash
python manage.py migrate --fake-initial
```

**Réinitialiser la base de données :**
```bash
# Supprimer db.sqlite3
# Puis :
python manage.py migrate
python manage.py createsuperuser
python manage.py init_data
```

**Problème avec les PDF :**
Vérifiez que ReportLab est installé :
```bash
pip install reportlab
```

## 📄 Licence

Ce projet est libre d'utilisation pour les cabinets médicaux.

## 🤝 Contribution

Pour proposer des améliorations :
1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Commitez vos changements
4. Proposez une Pull Request

---

## ✅ Application validée et nettoyée

L'application a été **entièrement validée, nettoyée et optimisée** :

### 🔧 Améliorations apportées :
- ✅ **Code nettoyé** - Suppression des `console.log` et `alert()`
- ✅ **Gestion d'erreurs renforcée** - Validation des modèles et formulaires
- ✅ **Génération PDF des factures** - Fonctionnalité complètement implémentée
- ✅ **Configuration du cabinet** - Système de configuration centralisé
- ✅ **Validation automatique** - Script de validation et nettoyage inclus
- ✅ **Sécurité renforcée** - Validations et contrôles ajoutés
- ✅ **Fichiers temporaires nettoyés** - Cache et fichiers inutiles supprimés

### 🎯 Nouvelles fonctionnalités :
- **Configuration dynamique** du cabinet via `/admin/`
- **Génération PDF** des ordonnances et factures personnalisées
- **Validation automatique** des données avec le script `validate_and_clean.py`
- **Interface d'administration** enrichie avec configuration du cabinet

### 🚀 Commandes utiles :

**Valider et nettoyer l'application :**
```bash
python validate_and_clean.py
```

**Configurer le cabinet :**
```bash
python manage.py init_config --nom-medecin "Dr. Votre Nom" --nom-cabinet "Votre Cabinet"
```

**Créer un superutilisateur :**
```bash
python manage.py createsuperuser
```

**Développé spécialement pour les cabinets médicaux au Maroc** 🇲🇦
