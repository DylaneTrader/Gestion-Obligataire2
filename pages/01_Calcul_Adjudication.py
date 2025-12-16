# app/pages/01_Calcul_Adjudication.py

import streamlit as st
import pandas as pd
from utils.common import set_page_config, display_header
from utils.adjudication import calculate_marginal_price

set_page_config()
display_header("Calcul d'Adjudication à Prix Multiple", "⚖️")

st.markdown("""
    Cette page permet de calculer le **prix marginal** et les **allocations** pour une adjudication
    d'obligations basée sur le principe du prix multiple.
""")

# --- Saisie des données ---
st.subheader("Paramètres de l'Adjudication")
total_amount = st.number_input("Montant Total à Allouer (en millions)", min_value=1.0, value=100.0, step=10.0)

st.subheader("Soumissions (Bids)")
st.info("Entrez les soumissions avec le prix (en pourcentage du nominal) et le montant demandé.")

# Créer un DataFrame éditable pour les soumissions
initial_data = pd.DataFrame({
    'Price': [99.50, 99.45, 99.40, 99.35],
    'Amount': [50.0, 75.0, 100.0, 50.0]
})

edited_df = st.data_editor(
    initial_data,
    num_rows="dynamic",
    column_config={
        "Price": st.column_config.NumberColumn("Prix (%)", format="%.2f", min_value=0.0),
        "Amount": st.column_config.NumberColumn("Montant Demandé (M€)", format="%.1f", min_value=0.0)
    },
    hide_index=True
)

# --- Calcul et Affichage des Résultats ---
if st.button("Calculer l'Adjudication"):
    if edited_df.empty:
        st.warning("Veuillez entrer au moins une soumission.")
    else:
        try:
            # Assurer que les colonnes sont numériques
            edited_df['Price'] = pd.to_numeric(edited_df['Price'], errors='coerce')
            edited_df['Amount'] = pd.to_numeric(edited_df['Amount'], errors='coerce')
            
            # Supprimer les lignes avec des valeurs manquantes après conversion
            bids_df = edited_df.dropna()
            
            if bids_df.empty:
                st.error("Les données de soumission sont invalides. Veuillez vérifier les entrées.")
            else:
                marginal_price, allocations_df = calculate_marginal_price(bids_df, total_amount)
                
                st.success("Calcul effectué avec succès!")
                
                st.subheader("Résultats de l'Adjudication")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Prix Marginal", f"{marginal_price:.2f} %")
                with col2:
                    st.metric("Montant Total Alloué", f"{allocations_df['Allocation'].sum():.2f} M€")
                
                st.markdown("### Détail des Allocations")
                
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
                
                st.markdown(f"""
                    <div style="margin-top: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
                        **Règle d'Allocation :**
                        Toutes les soumissions au-dessus de **{marginal_price:.2f} %** sont allouées intégralement.
                        Les soumissions à **{marginal_price:.2f} %** reçoivent une allocation partielle de **{allocation_ratio:.2%}** (si applicable).
                        Les soumissions en dessous de **{marginal_price:.2f} %** ne reçoivent aucune allocation.
                    </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Une erreur est survenue lors du calcul : {e}")
