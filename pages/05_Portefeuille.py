# app/pages/05_Portefeuille.py

import streamlit as st
import pandas as pd
import numpy as np
from utils.common import set_page_config, display_header, get_bond_example_df
from utils.bonds import calculate_ytm, calculate_duration

set_page_config()
display_header("Analyse de Portefeuille Obligataire", "💼")

st.markdown("""
    Analysez les métriques clés de votre portefeuille obligataire, y compris la **Duration** et le **Rendement** agrégés.
""")

# --- Saisie des Données du Portefeuille ---
st.subheader("Composition du Portefeuille")

# Utiliser les données d'exemple
example_df = get_bond_example_df()
example_df['Quantité'] = [100, 50, 200]

st.info("Modifiez le tableau ci-dessous pour définir la composition de votre portefeuille.")

portfolio_df = st.data_editor(
    example_df,
    num_rows="dynamic",
    column_config={
        "ISIN": st.column_config.TextColumn("ISIN"),
        "Nominal": st.column_config.NumberColumn("Nominal (€)"),
        "Taux_Coupon": st.column_config.NumberColumn("Taux Coupon (%)", format="%.2f"),
        "Frequence_Coupon": st.column_config.NumberColumn("Fréquence Coupon (par an)"),
        "Maturite_Annees": st.column_config.NumberColumn("Maturité (Années)"),
        "Prix_Actuel": st.column_config.NumberColumn("Prix Actuel (€)"),
        "Quantité": st.column_config.NumberColumn("Quantité")
    },
    hide_index=True
)

# --- Calcul et Affichage des Résultats ---
if st.button("Analyser le Portefeuille"):
    if portfolio_df.empty:
        st.warning("Veuillez entrer au moins une obligation dans le portefeuille.")
    else:
        try:
            # Assurer que les colonnes sont numériques et non nulles
            cols_to_check = ['Nominal', 'Taux_Coupon', 'Frequence_Coupon', 'Maturite_Annees', 'Prix_Actuel', 'Quantité']
            for col in cols_to_check:
                portfolio_df[col] = pd.to_numeric(portfolio_df[col], errors='coerce')
            
            portfolio_df.dropna(subset=cols_to_check, inplace=True)
            
            if portfolio_df.empty:
                st.error("Les données du portefeuille sont invalides. Veuillez vérifier les entrées.")
            else:
                # Calcul des métriques pour chaque obligation
                results = []
                for index, row in portfolio_df.iterrows():
                    ytm = calculate_ytm(
                        row['Prix_Actuel'], row['Nominal'], row['Taux_Coupon'] / 100, 
                        row['Frequence_Coupon'], row['Maturite_Annees']
                    )
                    macaulay, modified = calculate_duration(
                        row['Prix_Actuel'], row['Nominal'], row['Taux_Coupon'] / 100, 
                        row['Frequence_Coupon'], row['Maturite_Annees'], ytm
                    )
                    
                    market_value = row['Prix_Actuel'] * row['Quantité']
                    
                    results.append({
                        'ISIN': row['ISIN'],
                        'YTM': ytm,
                        'Modified_Duration': modified,
                        'Market_Value': market_value
                    })
                
                results_df = pd.DataFrame(results)
                
                # Calcul des métriques agrégées
                total_market_value = results_df['Market_Value'].sum()
                results_df['Weight'] = results_df['Market_Value'] / total_market_value
                
                # Duration Modifiée Pondérée du Portefeuille
                portfolio_duration = (results_df['Modified_Duration'] * results_df['Weight']).sum()
                
                # YTM Pondéré du Portefeuille (Approximation)
                portfolio_ytm = (results_df['YTM'] * results_df['Weight']).sum()
                
                st.success("Analyse du portefeuille effectuée avec succès!")
                
                st.subheader("Synthèse du Portefeuille")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Valeur Totale du Marché", f"{total_market_value:,.2f} €")
                with col2:
                    st.metric("Duration Modifiée du Portefeuille", f"{portfolio_duration:.2f} Années")
                with col3:
                    st.metric("YTM Pondéré du Portefeuille", f"{portfolio_ytm * 100:.2f} %")
                    
                st.markdown("### Détail des Obligations")
                
                # Affichage des détails
                detail_df = portfolio_df.copy()
                detail_df['YTM (%)'] = results_df['YTM'] * 100
                detail_df['Duration Modifiée'] = results_df['Modified_Duration']
                detail_df['Valeur Marché'] = results_df['Market_Value']
                detail_df['Poids (%)'] = results_df['Weight'] * 100
                
                st.dataframe(
                    detail_df[['ISIN', 'Quantité', 'Prix_Actuel', 'Valeur Marché', 'Poids (%)', 'YTM (%)', 'Duration Modifiée']],
                    hide_index=True
                )
                
        except Exception as e:
            st.error(f"Une erreur est survenue lors de l'analyse : {e}")
            st.exception(e)
