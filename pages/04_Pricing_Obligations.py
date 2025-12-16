# app/pages/04_Pricing_Obligations.py

import streamlit as st
from utils.common import set_page_config, display_header
from utils.bonds import calculate_ytm, calculate_price, calculate_duration

set_page_config()
display_header("Pricing et Analyse d'Obligations", "💰")

st.markdown("""
    Calculez le **Prix**, le **Rendement à l'Échéance (YTM)** et la **Duration** d'une obligation.
""")

# --- Saisie des Paramètres de l'Obligation ---
st.subheader("Paramètres de l'Obligation")

col1, col2, col3 = st.columns(3)
with col1:
    face_value = st.number_input("Valeur Nominale (€)", min_value=1.0, value=1000.0, step=100.0)
    coupon_rate = st.number_input("Taux de Coupon Annuel (%)", min_value=0.0, value=5.0, step=0.1) / 100
with col2:
    years_to_maturity = st.number_input("Années jusqu'à l'Échéance", min_value=0.1, value=5.0, step=0.5)
    frequency = st.selectbox("Fréquence de Paiement des Coupons", [1, 2, 4, 12], index=1, format_func=lambda x: f"{x} fois par an")
with col3:
    input_type = st.radio("Donnée d'Entrée pour le Calcul", ["Prix Actuel", "YTM Cible"])
    
    if input_type == "Prix Actuel":
        price = st.number_input("Prix Actuel (€)", min_value=0.0, value=980.0, step=1.0)
        ytm_target = None
    else:
        ytm_target = st.number_input("YTM Cible (%)", min_value=0.0, value=5.5, step=0.1) / 100
        price = None

# --- Calcul et Affichage des Résultats ---
if st.button("Calculer les Métriques"):
    try:
        if input_type == "Prix Actuel":
            # Calculer YTM et Duration à partir du Prix
            ytm = calculate_ytm(price, face_value, coupon_rate, frequency, years_to_maturity)
            macaulay, modified = calculate_duration(price, face_value, coupon_rate, frequency, years_to_maturity, ytm)
            
            st.subheader("Résultats (Calculé à partir du Prix)")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("Prix Actuel (€)", f"{price:.2f}")
            with col_res2:
                st.metric("Rendement à l'Échéance (YTM)", f"{ytm * 100:.2f} %")
            with col_res3:
                st.metric("Duration Modifiée (Années)", f"{modified:.2f}")
                
            st.info(f"Duration de Macaulay : {macaulay:.2f} années")
            
        else:
            # Calculer Prix et Duration à partir du YTM
            price_calc = calculate_price(ytm_target, face_value, coupon_rate, frequency, years_to_maturity)
            macaulay, modified = calculate_duration(price_calc, face_value, coupon_rate, frequency, years_to_maturity, ytm_target)
            
            st.subheader("Résultats (Calculé à partir du YTM Cible)")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            with col_res1:
                st.metric("YTM Cible", f"{ytm_target * 100:.2f} %")
            with col_res2:
                st.metric("Prix Calculé (€)", f"{price_calc:.2f}")
            with col_res3:
                st.metric("Duration Modifiée (Années)", f"{modified:.2f}")
                
            st.info(f"Duration de Macaulay : {macaulay:.2f} années")
            
        st.markdown("""
            <div style="margin-top: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
                **Interprétation de la Duration Modifiée :**
                Une Duration Modifiée de X signifie que pour une variation de 1% du YTM,
                le prix de l'obligation variera d'environ X%.
            </div>
        """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Une erreur est survenue lors du calcul : {e}")
