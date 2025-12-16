# app/pages/08_Aide_&_Concepts.py

import streamlit as st
from utils.common import set_page_config, display_header

set_page_config()
display_header("Aide et Concepts Clés", "📚")

st.markdown("""
    Cette section fournit des explications sur les concepts fondamentaux de la gestion obligataire
    utilisés dans cette application.
""")

# --- Section 1: Adjudication ---
st.subheader("1. Adjudication à Prix Multiple")
st.markdown("""
    L'adjudication à prix multiple est une méthode d'émission d'obligations où les soumissionnaires
    retenus paient le prix qu'ils ont soumis.
    
    *   **Prix Marginal :** C'est le prix le plus bas accepté par l'émetteur pour atteindre le montant total
        à allouer. Toutes les soumissions à ce prix reçoivent une allocation partielle.
    *   **Allocation :** Les soumissions au-dessus du prix marginal sont allouées intégralement.
        Les soumissions au prix marginal sont allouées au prorata du montant restant à allouer.
""")

# --- Section 2: Pricing et YTM ---
st.subheader("2. Rendement à l'Échéance (YTM)")
st.markdown("""
    Le **YTM (Yield to Maturity)** est le taux de rendement interne (TRI) d'une obligation,
    en supposant que l'investisseur détient l'obligation jusqu'à l'échéance et que tous les
    paiements de coupons sont réinvestis au même taux.
    
    Il est calculé en résolvant l'équation de la valeur actuelle :
    
    $$
    P = \\sum_{t=1}^{N} \\frac{C}{(1 + YTM/f)^t} + \\frac{FV}{(1 + YTM/f)^N}
    $$
    
    Où :
    *   $P$ = Prix actuel de l'obligation
    *   $C$ = Paiement de coupon périodique
    *   $FV$ = Valeur nominale (Face Value)
    *   $N$ = Nombre total de périodes
    *   $f$ = Fréquence de paiement des coupons par an
""")

# --- Section 3: Duration ---
st.subheader("3. Duration Modifiée")
st.markdown("""
    La **Duration Modifiée** est une mesure de la sensibilité du prix d'une obligation
    aux variations de son rendement (YTM).
    
    $$
    Duration Modifiée = \\frac{Duration de Macaulay}{1 + YTM/f}
    $$
    
    *   Elle est exprimée en années.
    *   Une Duration Modifiée de $X$ signifie que pour une augmentation de $1\%$ du YTM,
        le prix de l'obligation diminuera d'environ $X\%$.
""")

# --- Section 4: Courbe de Rendement ---
st.subheader("4. Courbe de Rendement (Yield Curve)")
st.markdown("""
    La courbe de rendement est une représentation graphique de la relation entre le rendement
    des obligations et leur maturité.
    
    *   **Courbe Normale (Pente Positive) :** Les rendements à long terme sont supérieurs aux rendements à court terme.
        C'est la forme la plus courante, indiquant des attentes de croissance économique.
    *   **Courbe Inversée (Pente Négative) :** Les rendements à court terme sont supérieurs aux rendements à long terme.
        C'est souvent un indicateur avancé de récession économique.
""")

st.info("Pour toute question technique ou conceptuelle supplémentaire, veuillez contacter votre expert en finance quantitative.")
