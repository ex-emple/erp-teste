# 🏥 ERP Médical - Système Unifié

> **Version 2.0** - Architecture consolidée et modularisée

Un système ERP complet pour la gestion d'un cabinet médical, développé avec Django 5.2.4. Cette version consolidée élimine toutes les redondances et implémente une architecture professionnelle basée sur des services.

## 📋 Table des Matières

- [🏗️ Architecture](#️-architecture)
- [🚀 Installation](#-installation)
- [💻 Utilisation](#-utilisation)
- [🔧 Gestion et Maintenance](#-gestion-et-maintenance)
- [📊 Fonctionnalités](#-fonctionnalités)
- [🏛️ Structure du Projet](#️-structure-du-projet)
- [🔗 API](#-api)
- [🧪 Tests](#-tests)
- [📝 Contribution](#-contribution)

## 🏗️ Architecture

### Principes de Conception

- **Architecture en Services** : Logique métier centralisée dans des services réutilisables
- **DRY (Don't Repeat Yourself)** : Élimination complète de la duplication de code
- **SOLID** : Respect des principes de programmation orientée objet
- **Modularité** : Composants indépendants et interchangeables
- **Scalabilité** : Architecture préparée pour la montée en charge

### Composants Principaux

```
ERP Médical
├── 🏥 Services Médicaux
│   ├── PatientService
│   ├── RendezVousService
│   ├── ConsultationService
│   ├── FacturationService
│   └── StatisticsService
├── 🔧 Services Administratifs
│   ├── UserManagementService
│   ├── SystemMaintenanceService
│   └── NotificationService
├── 🛠️ Utilitaires Communs
│   ├── IPAddressHelper
│   ├── RequestLogger
│   ├── PerformanceTracker
│   ├── SecurityHelper
│   └── CacheHelper
└── 🌐 Vues Unifiées
    ├── Class-Based Views
    ├── API REST
    └── Compatibilité Legacy
```

## 🚀 Installation

### Prérequis

- Python 3.8+
- Django 5.2.4
- Base de données (SQLite par défaut, PostgreSQL recommandé)

### Installation Rapide

```bash
# 1. Cloner le projet
git clone [repository-url]
cd mini-erp-docteur

# 2. Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configuration initiale
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser

# 5. Démarrer le serveur
python manage.py runserver
```

### Configuration Avancée

1. **Variables d'environnement** (optionnel) :
   ```bash
   cp .env.example .env
   # Éditer .env avec vos paramètres
   ```

2. **Base de données PostgreSQL** (recommandé) :
   ```python
   # Dans config/settings.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'erp_medical',
           'USER': 'votre_user',
           'PASSWORD': 'votre_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## 💻 Utilisation

### Interface Web

1. **Accès** : http://localhost:8000
2. **Connexion** : Utilisez le superuser créé lors de l'installation
3. **Navigation** : Interface intuitive avec tableau de bord unifié

### Gestionnaire Unifié (CLI)

Le script `manage_erp.py` remplace tous les anciens scripts de gestion :

```bash
# Tests complets du système
python manage_erp.py test

# Validation de l'intégrité
python manage_erp.py validate

# Nettoyage du système
python manage_erp.py cleanup

# Sauvegarde de la base
python manage_erp.py backup

# Vérification de santé
python manage_erp.py health

# Création de données de démo
python manage_erp.py demo --count 20

# Statistiques
python manage_erp.py stats
```

### Commandes Django Unifiées

```bash
# Gestionnaire via commande Django
python manage.py erp_manager create_sample_data --count 50
python manage.py erp_manager validate_system
python manage.py erp_manager cleanup --days 30
python manage.py erp_manager backup
python manage.py erp_manager health_check
python manage.py erp_manager statistics
```

## 🔧 Gestion et Maintenance

### Surveillance Système

- **Health Check** : Vérification automatique de la santé système
- **Métriques** : CPU, mémoire, disque, performance base de données
- **Alertes** : Notifications automatiques en cas de problème
- **Logs** : Système de logging centralisé et structuré

### Sauvegarde et Restauration

```bash
# Sauvegarde automatique
python manage_erp.py backup

# Sauvegarde manuelle avec timestamp
python manage.py dumpdata --natural-foreign --natural-primary > backup_$(date +%Y%m%d_%H%M%S).json

# Restauration
python manage.py loaddata backup_file.json
```

### Maintenance Préventive

```bash
# Nettoyage hebdomadaire (automatisé avec cron)
0 2 * * 0 cd /path/to/erp && python manage_erp.py cleanup --force

# Sauvegarde quotidienne
0 1 * * * cd /path/to/erp && python manage_erp.py backup

# Vérification de santé quotidienne
0 8 * * * cd /path/to/erp && python manage_erp.py health
```

## 📊 Fonctionnalités

### Gestion Médicale

- **👥 Patients** : Dossiers complets, historique, recherche avancée
- **📅 Rendez-vous** : Planning interactif, gestion des conflits, rappels
- **🩺 Consultations** : Saisie détaillée, templates, historique
- **💊 Ordonnances** : Création rapide, templates, génération PDF
- **🧾 Facturation** : Facturation automatique, suivi des paiements

### Administration

- **👤 Utilisateurs** : Gestion des rôles et permissions
- **📈 Statistiques** : KPIs en temps réel, rapports détaillés
- **🔒 Sécurité** : Audit, logs d'accès, surveillance
- **🔧 Maintenance** : Outils de diagnostic et réparation

### APIs

- **🔍 Recherche** : API de recherche patients en temps réel
- **📊 Statistiques** : APIs pour tableaux de bord externes
- **📅 Planning** : Gestion des créneaux et disponibilités

## 🏛️ Structure du Projet

```
mini-erp-docteur/
├── 📁 config/                    # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── 📁 core/                      # Application principale
│   ├── 📁 models/               # Modèles de données
│   ├── 📁 services/             # Services métier
│   │   ├── medical_services.py  # Services médicaux
│   │   ├── admin_services.py    # Services administratifs
│   │   └── __init__.py
│   ├── 📁 views/                # Vues unifiées
│   │   ├── unified_views.py     # Class-based views modernes
│   │   └── __init__.py
│   ├── 📁 urls/                 # URLs consolidées
│   │   └── unified_urls.py
│   ├── 📁 utils/                # Utilitaires communs
│   │   └── common_helpers.py    # Helpers centralisés
│   ├── 📁 middleware/           # Middleware refactorisé
│   ├── 📁 templates/            # Templates HTML
│   ├── 📁 static/               # Fichiers statiques
│   ├── 📁 management/           # Commandes Django
│   │   └── commands/
│   │       └── erp_manager.py   # Commande unifiée
│   └── 📁 tests/                # Tests unifiés
│       └── test_unified.py      # Suite de tests complète
├── 📁 logs/                     # Fichiers de logs
├── 📁 backups/                  # Sauvegardes automatiques
├── 📄 manage_erp.py             # Script de gestion unifié
├── 📄 requirements.txt          # Dépendances Python
├── 📄 README.md                 # Documentation (ce fichier)
└── 📄 manage.py                 # Gestionnaire Django standard
```

### Changements d'Architecture v2.0

#### ✅ Consolidations Réalisées

1. **Services Centralisés** :
   - `medical_services.py` : Tous les services médicaux
   - `admin_services.py` : Services administratifs
   - Élimination de la duplication de logique métier

2. **Utilitaires Unifiés** :
   - `common_helpers.py` : Fonctions communes (IPAddressHelper, etc.)
   - Suppression de 3 copies de `get_client_ip()`
   - Helpers réutilisables pour tous les composants

3. **Vues Modernisées** :
   - `unified_views.py` : Class-based views avec services
   - APIs REST intégrées
   - Élimination des vues dupliquées

4. **Tests Consolidés** :
   - `test_unified.py` : Suite de tests complète
   - Remplacement de `test_complete.py`, `test_systeme_complet.py`, `validate_and_clean.py`

5. **Scripts Unifiés** :
   - `manage_erp.py` : Remplace tous les scripts de gestion
   - `erp_manager.py` : Commande Django centralisée

#### ❌ Anciens Fichiers Remplacés

- ~~`test_complete.py`~~ → `test_unified.py`
- ~~`test_systeme_complet.py`~~ → `manage_erp.py test`
- ~~`validate_and_clean.py`~~ → `manage_erp.py validate`
- ~~Vues dupliquées~~ → `unified_views.py`
- ~~Middleware avec duplication~~ → Middleware refactorisé avec `common_helpers.py`

## 🔗 API

### Endpoints Principaux

```http
# Recherche de patients
GET /api/patients/search/?q=nom_patient

# Statistiques
GET /api/statistics/?period=today
GET /api/statistics/?period=month&year=2024&month=1

# Mise à jour statut RDV
POST /api/rdv/{id}/status/
Content-Type: application/json
{
    "statut": "confirme"
}
```

### Exemples d'Usage

```javascript
// Recherche de patients en temps réel
fetch('/api/patients/search/?q=Martin')
    .then(response => response.json())
    .then(data => {
        console.log(data.patients);
    });

// Récupération des statistiques
fetch('/api/statistics/?period=today')
    .then(response => response.json())
    .then(data => {
        console.log(data.statistics);
    });
```

## 🧪 Tests

### Exécution des Tests

```bash
# Tests complets avec le gestionnaire unifié
python manage_erp.py test --verbose

# Tests Django standards
python manage.py test

# Tests spécifiques
python manage.py test core.tests.test_unified

# Tests avec couverture
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Types de Tests

- **Tests d'Intégration** : Fonctionnalités complètes
- **Tests Unitaires** : Services et utilitaires
- **Tests de Performance** : Temps de réponse et charge
- **Tests de Sécurité** : Vulnérabilités et permissions

## 📈 Monitoring et Performance

### Métriques Surveillées

- **Performance Base de Données** : Temps de réponse des requêtes
- **Utilisation Ressources** : CPU, RAM, disque
- **Erreurs Application** : Logs d'erreurs et exceptions
- **Sécurité** : Tentatives d'accès non autorisées

### Optimisations Implémentées

- **Cache Intelligent** : Cache des requêtes fréquentes
- **Requêtes Optimisées** : `select_related` et `prefetch_related`
- **Pagination** : Limitation automatique des résultats
- **Compression** : Compression GZIP des réponses

## 🔒 Sécurité

### Mesures Implémentées

- **Authentification** : Système de login sécurisé
- **Autorisation** : Permissions basées sur les rôles
- **Audit Trail** : Logs de toutes les actions utilisateur
- **Protection CSRF** : Tokens CSRF sur tous les formulaires
- **Validation Données** : Validation côté serveur stricte

### Configuration Sécurisée

```python
# settings.py
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

## 🚀 Déploiement Production

### Checklist Déploiement

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` personnalisée
- [ ] Base de données PostgreSQL
- [ ] Serveur web (Nginx + Gunicorn)
- [ ] HTTPS configuré
- [ ] Sauvegardes automatiques
- [ ] Monitoring activé

### Configuration Nginx

```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name votre-domaine.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /path/to/staticfiles/;
    }
}
```

### Service Systemd

```ini
[Unit]
Description=ERP Medical Django App
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/path/to/erp
ExecStart=/path/to/venv/bin/gunicorn config.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📝 Contribution

### Standards de Code

- **PEP 8** : Respect strict des conventions Python
- **Type Hints** : Annotations de type obligatoires
- **Docstrings** : Documentation complète des fonctions
- **Tests** : Couverture de code > 80%

### Processus de Contribution

1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Commiter** les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. **Pousser** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Créer** une Pull Request

### Architecture des Commits

```
type(scope): description

feat(patients): ajout recherche avancée par critères multiples
fix(rdv): correction conflit horaires dans le planning
docs(readme): mise à jour documentation API
refactor(services): consolidation services de facturation
test(models): ajout tests unitaires pour Patient model
```

## 📞 Support

### Ressources

- **Documentation** : [Lien vers documentation complète]
- **Issues** : [Lien vers GitHub Issues]
- **Discussions** : [Lien vers forum de discussion]

### Contact

- **Email** : support@erp-medical.com
- **Discord** : [Lien vers serveur Discord]
- **Stack Overflow** : Tag `erp-medical`

---

## 🏆 Crédits

Développé avec ❤️ pour la communauté médicale.

### Technologies Utilisées

- **Django 5.2.4** - Framework web Python
- **Bootstrap 5** - Framework CSS
- **Chart.js** - Graphiques interactifs
- **ReportLab** - Génération PDF
- **PostgreSQL** - Base de données (recommandée)

### Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

> **Version 2.0** - Architecture consolidée | Dernière mise à jour: $(date)
