# Guide de déploiement Replit pour Mini ERP Docteur

## 🚀 Commandes de lancement configurées

Votre application est maintenant prête pour Replit avec les commandes suivantes :

### **Commande principale (automatique):**
```bash
python main.py
```

### **Commandes alternatives:**
```bash
# Démarrage simple
python manage.py runserver 0.0.0.0:8000

# Avec configuration Replit
python manage.py runserver 0.0.0.0:8000 --settings=config.settings_replit
```

## 📁 Fichiers créés pour Replit

✅ **`.replit`** - Configuration principale Replit  
✅ **`replit.nix`** - Dépendances système  
✅ **`main.py`** - Point d'entrée automatisé  
✅ **`config/settings_replit.py`** - Settings optimisés pour Replit  
✅ **`.env`** - Variables d'environnement  
✅ **`requirements.txt`** - Dépendances Python mises à jour  

## 🔧 Configuration automatique

Le fichier `main.py` effectue automatiquement :
1. ✅ Migration de la base de données
2. ✅ Collecte des fichiers statiques
3. ✅ Création de données de test (si base vide)
4. ✅ Démarrage du serveur Django

## 🌐 URLs après déploiement

Une fois déployé sur Replit, votre application sera accessible via :
- **Application principale:** `https://votre-repl.username.repl.co/`
- **Interface admin:** `https://votre-repl.username.repl.co/admin/`
- **Gestion patients:** `https://votre-repl.username.repl.co/patients/`
- **Dashboard KPI:** `https://votre-repl.username.repl.co/dashboard/`

## 📝 Instructions de déploiement

### **1. Créer un nouveau Repl**
1. Allez sur **replit.com**
2. Cliquez **"Create Repl"**
3. Sélectionnez **"Python"**
4. Nommez votre projet : `erp-medical-docteur`

### **2. Importer votre code**
- Uploadez tous les fichiers de votre dossier `mini erp docteur`
- Ou connectez votre repository GitHub

### **3. Configuration automatique**
- Replit détectera le fichier `.replit`
- Les dépendances seront installées automatiquement
- Le serveur se lancera avec `python main.py`

### **4. Variables d'environnement (optionnel)**
Dans l'onglet "Secrets" de Replit :
- `SECRET_KEY` : `django-insecure-votre-cle-secrete-super-longue`
- `DEBUG` : `False` (pour la production)

## ⚡ Fonctionnalités Replit

- ✅ **Auto-redémarrage** à chaque modification
- ✅ **HTTPS automatique** 
- ✅ **URL publique** permanente
- ✅ **Base SQLite** persistante
- ✅ **Fichiers statiques** optimisés avec WhiteNoise

## 🏥 Données de test incluses

Au premier lancement, l'application créera automatiquement :
- 3 patients de démonstration
- Interface complète fonctionnelle
- Toutes les fonctionnalités ERP opérationnelles

## 🔍 Dépannage

Si problème au lancement :
1. Vérifiez les logs dans la console Replit
2. Assurez-vous que tous les fichiers sont uploadés
3. Vérifiez que le fichier `.replit` est présent

Votre Mini ERP Docteur est maintenant prêt pour Replit ! 🏥✨
