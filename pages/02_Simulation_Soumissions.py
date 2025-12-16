# app/pages/02_Simulation_Soumissions.py

import streamlit as st
import pandas as pd
import numpy as np
from utils.common import set_page_config, display_header
from utils.adjudication import calculate_marginal_price

set_page_config()
display_header("Simulation de Soumissions à l'Adjudication", "🎲")

st.markdown("""
    Cette page permet de simuler l'impact de vos propres soumissions sur le résultat d'une adjudication,
    en considérant les soumissions du marché (agrégées).
""")

# --- Saisie des données du Marché ---
st.subheader("Soumissions du Marché (Agrégées)")
st.info("Entrez les soumissions agrégées du marché (hors votre soumission).")

market_data = pd.DataFrame({
    'Price': [99.55, 99.50, 99.45, 99.40, 99.35],
    'Amount': [80.0, 120.0, 150.0, 100.0, 50.0]
})

market_df = st.data_editor(
    market_data,
    num_rows="dynamic",
    key="market_bids",
    column_config={
        "Price": st.column_config.NumberColumn("Prix (%)", format="%.2f", min_value=0.0),
        "Amount": st.column_config.NumberColumn("Montant Demandé (M€)", format="%.1f", min_value=0.0)
    },
    hide_index=True
)

# --- Saisie de la Soumission de l'Utilisateur ---
st.subheader("Votre Soumission")
user_price = st.number_input("Votre Prix (%)", min_value=0.0, value=99.40, step=0.01)
user_amount = st.number_input("Votre Montant Demandé (M€)", min_value=0.0, value=50.0, step=1.0)

# --- Paramètres de l'Adjudication ---
st.subheader("Paramètres Généraux")
total_amount = st.number_input("Montant Total à Allouer (M€)", min_value=1.0, value=500.0, step=10.0)

# --- Calcul et Affichage des Résultats ---
if st.button("Simuler l'Adjudication"):
    try:
        # 1. Préparer les DataFrames
        market_df['Price'] = pd.to_numeric(market_df['Price'], errors='coerce')
        market_df['Amount'] = pd.to_numeric(market_df['Amount'], errors='coerce')
        market_df.dropna(inplace=True)
        
        user_bid = pd.DataFrame({'Price': [user_price], 'Amount': [user_amount]})
        
        # 2. Combiner les soumissions
        all_bids = pd.concat([market_df, user_bid], ignore_index=True)
        
        # 3. Calculer l'adjudication
        marginal_price, allocations_df = calculate_marginal_price(all_bids, total_amount)
        
        st.success("Simulation effectuée avec succès!")
        
        st.subheader("Résultats de la Simulation")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Prix Marginal", f"{marginal_price:.2f} %")
        with col2:
            st.metric("Montant Total Alloué", f"{allocations_df['Allocation'].sum():.2f} M€")
            
        # 4. Extraire l'allocation de l'utilisateur
        user_allocation = allocations_df[allocations_df['Price'] == user_price]['Allocation'].sum()
        
        st.markdown("### Votre Résultat")
        
        col3, col4 = st.columns(2)
        with col3:
            st.metric("Votre Montant Alloué", f"{user_allocation:.2f} M€")
        with col4:
            allocation_ratio = user_allocation / user_amount if user_amount > 0 else 0
            st.metric("Ratio d'Allocation", f"{allocation_ratio:.2%}")
            
        st.markdown("### Détail des Allocations (Incluant Votre Soumission)")
        
        # Mise en forme du DataFrame pour l'affichage
        allocations_display = allocations_df.copy()
        allocations_display['Allocation Ratio'] = (allocations_display['Allocation'] / allocations_display['Amount']).apply(lambda x: f"{x:.2%}" if x > 0 else "0.00%")
        allocations_display.rename(columns={
            'Price': 'Prix (%)',
            'Amount': 'Montant Demandé (M€)',
            'Allocation': 'Montant Alloué (M€)'
        }, inplace=True)
        
        st.dataframe(
            allocations_display[['Prix (%)', 'Montant Demandé (M€)', 'Montant Alloué (M€)', 'Allocation Ratio']],
            hide_index=True
        )
        
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la simulation : {e}")
