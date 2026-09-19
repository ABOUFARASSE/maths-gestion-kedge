# Guide rapide de publication

## Objectif

Mettre l'application à disposition des étudiants au moyen d'une adresse web. Les étudiants n'installent rien et n'ont pas besoin de compte GitHub.

## 1. Tester l'application sur votre ordinateur

1. Installer Python 3.11 ou 3.12.
2. Décompresser le dossier.
3. Ouvrir un terminal dans le dossier.
4. Exécuter sous Windows :

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Le navigateur s'ouvre normalement sur `http://localhost:8501`.

## 2. Créer le dépôt GitHub

1. Se connecter à GitHub.
2. Cliquer sur **New repository**.
3. Nom conseillé : `maths-gestion-kedge`.
4. Choisir un dépôt public si l'application doit être déployée gratuitement et partagée facilement.
5. Importer le contenu du dossier, sans ajouter un niveau de dossier supplémentaire.

À la racine du dépôt, on doit voir directement `app.py`, `maths.py`, `requirements.txt` et `README.md`.

## 3. Déployer l'application

1. Ouvrir Streamlit Community Cloud.
2. Se connecter avec GitHub.
3. Sélectionner **Create app**.
4. Choisir le dépôt `maths-gestion-kedge`.
5. Choisir la branche `main`.
6. Renseigner `app.py` comme fichier principal.
7. Cliquer sur **Deploy**.

## 4. Partager avec les étudiants

Insérer l'adresse publique :

- dans le syllabus ;
- sur Moodle ou Blackboard ;
- dans les diapositives ;
- dans un QR code affiché en classe.

## 5. Mettre à jour

Une modification envoyée sur la branche principale du dépôt est répercutée sur l'application après redéploiement automatique.

## Point important

GitHub Pages publie des pages statiques mais n'exécute pas directement une application Python Streamlit. Le dépôt est placé sur GitHub et l'exécution est assurée par Streamlit Community Cloud.
