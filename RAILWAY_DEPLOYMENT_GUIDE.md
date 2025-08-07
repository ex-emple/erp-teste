# Guide de déploiement Railway pour Mini ERP Docteur

## 🚂 Déploiement sur Railway.app

### **Étape 1: Préparation du code**

✅ **Fichiers créés pour Railway:**
- `config/settings_railway.py` - Configuration optimisée Railway
- `railway.json` - Configuration de déploiement
- `railway_start.py` - Script d'initialisation
- `requirements.txt` - Dépendances mises à jour
- `Procfile` - Commandes de démarrage
- `.env.railway` - Variables d'environnement

### **Étape 2: Push sur GitHub**

```bash
# Si pas encore fait, initialisez Git
git init
git add .
git commit -m "Configuration Railway pour ERP Médical"

# Créez un repository sur GitHub et push
git remote add origin https://github.com/votre-username/erp-medical-docteur.git
git branch -M main
git push -u origin main
```

### **Étape 3: Déploiement sur Railway**

1. **Allez sur https://railway.app**
2. **Connectez votre compte GitHub**
3. **Cliquez "New Project"**
4. **Sélectionnez "Deploy from GitHub repo"**
5. **Choisissez votre repository `erp-medical-docteur`**

### **Étape 4: Configuration automatique**

Railway détectera automatiquement :
- ✅ **Python/Django** - Configuration auto
- ✅ **Requirements.txt** - Installation des dépendances
- ✅ **Procfile** - Commandes de build et start

### **Étape 5: Ajouter une base de données PostgreSQL**

1. **Dans votre projet Railway, cliquez "New"**
2. **Sélectionnez "Database" → "PostgreSQL"**
3. **Railway créera automatiquement:**
   - Base de données PostgreSQL
   - Variable `DATABASE_URL` 
   - Connexion automatique à votre app

### **Étape 6: Variables d'environnement**

Dans l'onglet "Variables" de votre service web :

```
SECRET_KEY=django-insecure-votre-cle-secrete-de-50-caracteres-minimum
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings_railway
```

### **Étape 7: Déploiement automatique**

- ✅ Railway build et deploy automatiquement
- ✅ Migrations exécutées automatiquement
- ✅ Fichiers statiques collectés
- ✅ Données de test créées (si base vide)

## 🌐 URLs après déploiement

Votre application sera accessible via :
- **App principale:** `https://votre-app.up.railway.app/`
- **Interface admin:** `https://votre-app.up.railway.app/admin/`
- **Gestion patients:** `https://votre-app.up.railway.app/patients/`
- **Dashboard KPI:** `https://votre-app.up.railway.app/dashboard/`

## 📊 Fonctionnalités Railway

- ✅ **Auto-deploy** - À chaque push GitHub
- ✅ **PostgreSQL gratuit** - 1GB de stockage
- ✅ **SSL automatique** - HTTPS inclus
- ✅ **Logs en temps réel** - Debug facile
- ✅ **Scaling automatique** - Performance adaptative
- ✅ **Domaine custom** - Configurez votre propre domaine

## 🛠️ Maintenance et updates

### **Mise à jour de l'application:**
```bash
git add .
git commit -m "Nouvelles fonctionnalités"
git push origin main
# Railway redéploie automatiquement !
```

### **Accès aux logs:**
- Dashboard Railway → Votre service → Onglet "Logs"
- Logs en temps réel pour debug

### **Exécuter des commandes:**
```bash
# Dans l'interface Railway, onglet "Shell"
python manage.py createsuperuser
python manage.py shell
python manage.py collectstatic
```

## 🔧 Configuration avancée

### **Variables d'environnement recommandées:**
```
SECRET_KEY=votre-cle-secrete-de-production
DEBUG=False
DJANGO_SETTINGS_MODULE=config.settings_railway
DJANGO_LOG_LEVEL=INFO
```

### **Commandes de build personnalisées:**
```json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "python railway_start.py"
  }
}
```

## 🏥 Données de test incluses

Au premier déploiement, l'application créera automatiquement :
- 3 patients de démonstration
- Consultations d'exemple
- Ordonnances de test
- Interface admin fonctionnelle

## 🚨 Troubleshooting

### **En cas d'erreur de build:**
1. Vérifiez les logs dans Railway
2. Assurez-vous que `requirements.txt` est correct
3. Vérifiez que le `settings_railway.py` est configuré

### **En cas d'erreur de base de données:**
1. Vérifiez que PostgreSQL est ajouté au projet
2. La variable `DATABASE_URL` doit être automatiquement définie
3. Les migrations s'exécutent au démarrage

### **Pour accéder à l'admin:**
```bash
# Dans le shell Railway
python manage.py createsuperuser
```

## ✨ Résultat final

Votre **Mini ERP Docteur** sera maintenant hébergé professionnellement sur Railway avec :
- 🏥 **Interface complète** de gestion médicale
- 📊 **Dashboard KPI** avec statistiques
- 👥 **Gestion des patients** avec suivi médical
- 📋 **Système de consultations** et ordonnances
- 🔒 **Interface admin** Django
- 📱 **Design responsive** Bootstrap

**URL de démo:** `https://votre-app.up.railway.app/patients/`

Votre ERP médical est maintenant en production ! 🚀🏥
