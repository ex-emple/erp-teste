# Guide de déploiement pour Mini ERP Docteur

## Options d'hébergement gratuit

### 1. Railway (Recommandé)
Railway offre un plan gratuit généreux et un déploiement simple.

**Étapes :**
1. Créez un compte sur https://railway.app
2. Connectez votre repository GitHub
3. Railway détectera automatiquement Django
4. Ajoutez ces variables d'environnement :
   - `SECRET_KEY`: Une clé secrète forte
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: votre-app.railway.app
   - `DJANGO_SETTINGS_MODULE`: config.settings_prod

### 2. Render
Render offre également un bon service gratuit.

**Étapes :**
1. Créez un compte sur https://render.com
2. Créez un nouveau "Web Service"
3. Connectez votre repository GitHub
4. Configurez :
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn config.wsgi:application`

### 3. Heroku (Plan gratuit limité)
Heroku reste une option mais avec des limitations.

**Étapes :**
1. Installez Heroku CLI
2. `heroku create votre-app-name`
3. `git push heroku main`
4. `heroku run python manage.py migrate`

## Préparation de votre application

### 1. Fichiers créés pour vous :
- ✅ `requirements.txt` - Dépendances Python
- ✅ `Procfile` - Configuration du serveur
- ✅ `runtime.txt` - Version Python
- ✅ `config/settings_prod.py` - Configuration production
- ✅ `.env.example` - Variables d'environnement
- ✅ `create_initial_data.py` - Données initiales

### 2. Variables d'environnement à configurer :

```
SECRET_KEY=votre-cle-secrete-de-50-caracteres-minimum
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
DATABASE_URL=postgres://user:pass@host:port/db
```

### 3. Commandes après déploiement :

```bash
# Migrations de la base de données
python manage.py migrate

# Création d'un superuser
python manage.py createsuperuser

# Collecte des fichiers statiques
python manage.py collectstatic --noinput

# Création de données initiales (optionnel)
python create_initial_data.py
```

## Sécurité en production

### Points importants :
- ✅ DEBUG=False configuré
- ✅ SECRET_KEY sécurisée
- ✅ ALLOWED_HOSTS configuré
- ✅ WhiteNoise pour les fichiers statiques
- ✅ Logs configurés
- ✅ Middleware de sécurité activé

### Base de données :
- Développement: SQLite (inclus)
- Production: PostgreSQL (recommandé)

## Workflow de déploiement

1. **Préparer le code**
   ```bash
   git add .
   git commit -m "Préparation pour déploiement"
   git push origin main
   ```

2. **Créer .env pour la production**
   ```bash
   cp .env.example .env
   # Modifiez .env avec vos vraies valeurs
   ```

3. **Déployer selon la plateforme choisie**

4. **Configurer la base de données**

5. **Tester l'application**

## Maintenance

### Logs d'application :
- Railway: Dashboard > Logs
- Render: Dashboard > Logs  
- Heroku: `heroku logs --tail`

### Mise à jour :
1. Modifiez votre code localement
2. Commitez et push sur GitHub
3. Le redéploiement est automatique

## Support

En cas de problème :
1. Vérifiez les logs de la plateforme
2. Vérifiez les variables d'environnement
3. Testez localement avec les settings de production

## URLs importantes après déploiement

- Admin: https://votre-app.com/admin/
- Patients: https://votre-app.com/patients/
- Dashboard: https://votre-app.com/dashboard/
