# Documentation de l'Application Streamlit de Gestion Obligataire

**Auteur :** Manus AI
**Date :** 9 Décembre 2025

## 1. Introduction

Cette documentation décrit l'architecture, l'installation et l'utilisation de l'application **Gestion Obligataire**, une interface utilisateur développée avec Streamlit. L'application est conçue pour les professionnels de la finance quantitative et les investisseurs, offrant des outils d'analyse et de gestion des instruments obligataires, notamment le calcul d'adjudication, le pricing, l'analyse de duration et la visualisation de la courbe de rendement.

L'application est structurée autour de huit pages thématiques, s'appuyant sur des modules Python dédiés pour les calculs financiers complexes.

## 2. Installation et Lancement

### 2.1. Prérequis

L'application nécessite un environnement Python 3.x. Les dépendances spécifiques sont listées dans le fichier `requirements.txt`.

### 2.2. Installation des Dépendances

Après avoir décompressé l'archive du projet, naviguez jusqu'au répertoire racine et installez les dépendances à l'aide de `pip` :

```bash
pip install -r requirements.txt
```

Les principales dépendances incluent :
*   `streamlit` : Pour l'interface utilisateur web.
*   `pandas` et `numpy` : Pour la manipulation et les calculs de données.
*   `plotly` : Pour la création de graphiques interactifs (Courbe de Rendement, Backtest).
*   `scipy` : Pour les fonctions mathématiques avancées (utilisées notamment pour l'interpolation de la courbe de rendement).
*   `openpyxl` : Pour la lecture des fichiers Excel (dans le module `utils/common.py`).

### 2.3. Lancement de l'Application

Lancez l'application depuis le répertoire parent du dossier `app/` :

```bash
streamlit run app/app.py
```

L'application s'ouvrira automatiquement dans votre navigateur web par défaut.

## 3. Architecture du Projet

Le projet suit une structure modulaire standard pour les applications Streamlit multi-pages, garantissant une séparation claire des préoccupations (UI, logique métier, données).

| Dossier/Fichier | Description |
| :--- | :--- |
| `app/` | Répertoire racine de l'application. |
| `app/app.py` | **Page d'accueil** de l'application. Sert de point d'entrée et de présentation générale. |
| `app/pages/` | Contient les fichiers Python pour chaque page de l'application. Streamlit les détecte et les affiche automatiquement dans la barre latérale. |
| `app/utils/` | Contient les modules Python pour la logique métier et les fonctions de calcul réutilisables. |
| `app/assets/` | Contient les ressources statiques telles que les feuilles de style CSS (`style.css`), les logos ou les icônes. |
| `app/data/` | Destiné à stocker les fichiers de données d'exemple ou les modèles de fichiers (ex: `exemple_obligations.xlsx`). |
| `requirements.txt` | Liste des dépendances Python. |

## 4. Détail des Modules Utilitaires (`app/utils/`)

Ces modules encapsulent la logique financière et les fonctions transversales, permettant aux pages de se concentrer sur l'interaction utilisateur et l'affichage.

### 4.1. `bonds.py` (Pricing, YTM, Duration)

Ce module contient les fonctions fondamentales pour l'analyse des obligations.

| Fonction | Description |
| :--- | :--- |
| `calculate_ytm(price, face_value, coupon_rate, frequency, years_to_maturity)` | Calcule le **Rendement à l'Échéance (YTM)** d'une obligation. Utilise une méthode d'approximation pour la simplicité de l'implémentation Streamlit. |
| `calculate_price(ytm, face_value, coupon_rate, frequency, years_to_maturity)` | Calcule le **Prix Théorique** d'une obligation en actualisant les flux de trésorerie futurs au taux YTM donné. |
| `calculate_duration(price, face_value, coupon_rate, frequency, years_to_maturity, ytm=None)` | Calcule la **Duration de Macaulay** et la **Duration Modifiée**. La Duration Modifiée est l'indicateur clé de la sensibilité du prix aux variations de taux. |

### 4.2. `adjudication.py` (Calcul Prix Marginal + Allocations)

Ce module gère la logique spécifique aux enchères d'obligations.

| Fonction | Description |
| :--- | :--- |
| `calculate_marginal_price(bids_df, total_amount)` | Détermine le **Prix Marginal** et calcule les **Allocations** pour chaque soumission dans le cadre d'une adjudication à prix multiple. Elle trie les soumissions, calcule le montant cumulé et applique la règle d'allocation au prorata au prix marginal. |

### 4.3. `yields.py` (Courbe de Rendement)

Ce module fournit les outils pour la gestion et l'analyse de la courbe de rendement.

| Fonction | Description |
| :--- | :--- |
| `create_dummy_yield_curve(maturities)` | Génère un jeu de données factice pour la courbe de rendement (à des fins de démonstration). |
| `interpolate_yield_curve(curve_df, target_maturities)` | Effectue une **interpolation** de la courbe de rendement en utilisant la méthode des **Splines Cubiques** (`scipy.interpolate.CubicSpline`) pour obtenir des rendements pour des maturités non observées. |

### 4.4. `common.py` (Fonctions Communes)

Ce module regroupe les fonctions utilitaires générales pour l'application Streamlit.

| Fonction | Description |
| :--- | :--- |
| `set_page_config()` | Configure les paramètres de base de la page Streamlit (titre, icône, layout). |
| `load_data(file_path)` | Fonction générique pour charger des données depuis des fichiers CSV ou Excel. |
| `display_header(title, icon)` | Affiche un en-tête stylisé pour chaque page. |
| `get_bond_example_df()` | Fournit un DataFrame d'exemple pour les obligations. |

## 5. Détail des Pages (`app/pages/`)

Chaque fichier dans le dossier `pages/` correspond à une page accessible via la barre latérale de l'application.

| Fichier | Titre de la Page | Fonctionnalité Principale |
| :--- | :--- | :--- |
| `01_Calcul_Adjudication.py` | Calcul d'Adjudication à Prix Multiple | Permet à l'utilisateur de saisir les soumissions du marché et le montant total à allouer pour déterminer le **Prix Marginal** et les **Allocations** finales. |
| `02_Simulation_Soumissions.py` | Simulation de Soumissions à l'Adjudication | Permet de simuler l'impact d'une soumission spécifique de l'utilisateur en la combinant avec les soumissions agrégées du marché, et d'analyser le ratio d'allocation obtenu. |
| `03_Yield_Curve.py` | Analyse de la Courbe de Rendement | Visualise la courbe de rendement (à partir de données d'exemple ou chargées). Utilise l'interpolation par splines cubiques et permet l'analyse de la pente (spread). |
| `04_Pricing_Obligations.py` | Pricing et Analyse d'Obligations | Calcule le **YTM** et la **Duration** à partir du prix de marché, ou le **Prix Théorique** et la **Duration** à partir d'un YTM cible. |
| `05_Portefeuille.py` | Analyse de Portefeuille Obligataire | Permet de saisir la composition d'un portefeuille et calcule les métriques agrégées clés : **Valeur Totale du Marché**, **Duration Modifiée Pondérée** et **YTM Pondéré**. |
| `06_Backtest_Adjudications.py` | Backtest de Stratégies d'Adjudication | (Maquette) Simule l'évaluation de la performance historique des stratégies de soumission en comparant les prix soumis aux prix marginaux réels simulés. |
| `07_Opportunités.py` | Identification d'Opportunités d'Arbitrage | Compare le prix de marché d'une obligation à son prix théorique (calculé à partir d'un YTM de référence) pour identifier si l'obligation est **sous-évaluée** (opportunité d'achat) ou **surévaluée** (opportunité de vente). |
| `08_Aide_&_Concepts.py` | Aide et Concepts Clés | Fournit une documentation intégrée à l'application, expliquant les concepts fondamentaux de la finance obligataire tels que le YTM, la Duration Modifiée et l'Adjudication à Prix Multiple. |

## 6. Utilisation des Données

L'application est conçue pour être interactive et utilise principalement la saisie directe de données via les widgets Streamlit (`st.data_editor`, `st.number_input`).

*   **Chargement de Fichiers :** La page `03_Yield_Curve.py` permet le chargement de fichiers CSV ou Excel pour les données de la courbe de rendement.
*   **Fichiers d'Exemple :** Le dossier `app/data/` contient des fichiers d'exemple (`exemple_obligations.xlsx`) pour faciliter les tests et la démonstration.

## 7. Style et Personnalisation

Le fichier `app/assets/style.css` contient des styles CSS personnalisés pour améliorer l'apparence de l'application, notamment :

*   Configuration de la police et du fond.
*   Stylisation des boutons primaires.
*   Mise en forme des en-têtes de page.

Pour personnaliser l'apparence, modifiez ce fichier CSS. Pour modifier la configuration de base de Streamlit, ajustez la fonction `set_page_config` dans `app/utils/common.py`.

---
*Fin de la documentation.*
