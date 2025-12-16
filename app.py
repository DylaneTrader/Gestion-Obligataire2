# app/app.py

import streamlit as st
from utils.common import set_page_config, display_header

# Configuration de la page
set_page_config()

# Chargement du CSS
with open("app/assets/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Contenu de la page d'accueil
display_header("Bienvenue dans l'Outil de Gestion Obligataire 📈", "🏠")

st.markdown("""
    <div style="font-size: 1.2em; margin-bottom: 20px;">
        Cet outil est conçu pour les professionnels de la finance quantitative et les investisseurs
        souhaitant analyser et gérer des portefeuilles obligataires.
    </div>
    
    <hr>
    
    ## Fonctionnalités Principales
    
    Utilisez le menu de navigation à gauche pour accéder aux différents modules :
    
    ### 1. Calculs d'Adjudication
    *   **Calcul Adjudication :** Déterminez le prix marginal et les allocations pour une adjudication à prix multiple.
    *   **Simulation Soumissions :** Simulez l'impact de différentes stratégies de soumission.
    
    ### 2. Analyse de Marché
    *   **Yield Curve :** Visualisez et analysez la courbe de rendement.
    *   **Pricing Obligations :** Calculez le prix, le YTM et la duration d'une obligation.
    
    ### 3. Gestion de Portefeuille
    *   **Portefeuille :** Gérez et analysez les risques de votre portefeuille obligataire.
    *   **Backtest Adjudications :** Évaluez la performance historique de vos stratégies.
    
    ### 4. Ressources
    *   **Opportunités :** Identifiez des opportunités d'arbitrage ou de trading.
    *   **Aide & Concepts :** Accédez à des explications détaillées sur les concepts clés.
    
    <br>
    
    **Expertise :** Cet outil est basé sur des principes de **finance quantitative** et de **programmation** pour vous fournir des analyses précises et robustes.
""", unsafe_allow_html=True)

# Afficher les pages dans la sidebar (automatiquement géré par Streamlit)
# st.sidebar.title("Navigation")
# Les pages sont listées automatiquement grâce à la structure de dossiers 'pages/'
