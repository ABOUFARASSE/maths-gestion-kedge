# Mathématiques appliquées à la gestion — KEDGE

Application pédagogique facultative destinée aux étudiants de première année. La version publiée par GitHub Pages utilise Pyodide : Python s'exécute directement dans le navigateur, sans serveur.

## Contenu

- Séance 1 : fractions, proportions, budget, remise et TVA ;
- Séance 2 : puissances, croissance composée et équations du premier degré ;
- Séance 3 : second degré, seuils de rentabilité et profit maximal ;
- Séance 4 : dérivées, coût marginal et recette marginale ;
- Séance 5 : étude de fonctions et optimisation sous contrainte ;
- cas intégrateur : prix, demande, capacité, coûts et profit.

Chaque page contient une situation de gestion, les calculs détaillés, une simulation, un graphique, une interprétation et un exercice corrigé.

## Lancer localement

```bash
python -m venv .venv
```

Sous Windows :

```bat
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Sous macOS ou Linux :

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publier avec GitHub Pages et Pyodide

1. Créer un nouveau dépôt GitHub.
2. Déposer tous les fichiers de ce dossier à la racine du dépôt.
3. Dans **Settings > Pages**, choisir **GitHub Actions** comme source.
4. Le workflow `.github/workflows/pages.yml` publie automatiquement `index.html`.
5. Partager l'adresse `https://<compte>.github.io/<depot>/` avec les étudiants.

`index.html` charge Pyodide et exécute les fonctions Python localement dans le navigateur. `app.py` reste disponible comme version Streamlit alternative.

## Structure

```text
.
├── app.py
├── maths.py
├── requirements.txt
├── README.md
├── tests/
│   └── test_maths.py
└── .streamlit/
    └── config.toml
```

## Principes pédagogiques

- ne jamais donner un résultat sans les étapes essentielles ;
- terminer chaque calcul par une interprétation de gestion ;
- distinguer solution mathématique et décision réalisable ;
- rendre visibles les hypothèses et les unités ;
- utiliser l'outil après un premier raisonnement manuel.

## Licence et données

Les données de l'application sont fictives et destinées exclusivement à l'apprentissage. Aucun résultat ne constitue un conseil financier ou commercial.
