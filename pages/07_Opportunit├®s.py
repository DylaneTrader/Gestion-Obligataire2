# app/pages/07_Opportunités.py

import streamlit as st
import pandas as pd
import numpy as np
from utils.common import set_page_config, display_header, get_bond_example_df
from utils.bonds import calculate_price

set_page_config()
display_header("Identification d'Opportunités d'Arbitrage", "🔍")

st.markdown("""
    Cette page simule la recherche d'opportunités d'arbitrage ou de trading en comparant
    le prix de marché d'une obligation à son prix théorique calculé à partir d'une courbe de rendement.
""")

# --- Saisie des Données ---
st.subheader("Données d'Obligations et YTM de Référence")

# Utiliser les données d'exemple
bonds_df = get_bond_example_df()
bonds_df['YTM_Reference (%)'] = [3.2, 5.1, 1.8] # YTM de référence pour la maturité correspondante

st.info("Entrez les obligations à analyser et leur YTM de référence (issu de la courbe de rendement).")

analysis_df = st.data_editor(
    bonds_df,
    num_rows="dynamic",
    column_config={
        "ISIN": st.column_config.TextColumn("ISIN"),
        "Nominal": st.column_config.NumberColumn("Nominal (€)"),
        "Taux_Coupon": st.column_config.NumberColumn("Taux Coupon (%)", format="%.2f"),
        "Frequence_Coupon": st.column_config.NumberColumn("Fréquence Coupon (par an)"),
        "Maturite_Annees": st.column_config.NumberColumn("Maturité (Années)"),
        "Prix_Actuel": st.column_config.NumberColumn("Prix de Marché (€)"),
        "YTM_Reference (%)": st.column_config.NumberColumn("YTM de Référence (%)", format="%.2f")
    },
    hide_index=True
)

# --- Calcul et Affichage des Résultats ---
if st.button("Rechercher les Opportunités"):
    if analysis_df.empty:
        st.warning("Veuillez entrer au moins une obligation à analyser.")
    else:
        try:
            # Assurer que les colonnes sont numériques
            cols_to_check = ['Nominal', 'Taux_Coupon', 'Frequence_Coupon', 'Maturite_Annees', 'Prix_Actuel', 'YTM_Reference (%)']
            for col in cols_to_check:
                analysis_df[col] = pd.to_numeric(analysis_df[col], errors='coerce')
            
            analysis_df.dropna(subset=cols_to_check, inplace=True)
            
            if analysis_df.empty:
                st.error("Les données d'analyse sont invalides. Veuillez vérifier les entrées.")
            else:
                # Calcul du prix théorique
                analysis_df['Prix_Théorique'] = analysis_df.apply(
                    lambda row: calculate_price(
                        row['YTM_Reference (%)'] / 100, 
                        row['Nominal'], 
                        row['Taux_Coupon'] / 100, 
                        row['Frequence_Coupon'], 
                        row['Maturite_Annees']
                    ), axis=1
                )
                
                # Calcul de l'écart (Spread)
                analysis_df['Écart_Prix'] = analysis_df['Prix_Actuel'] - analysis_df['Prix_Théorique']
                
                # Identification de l'opportunité
                analysis_df['Opportunité'] = np.where(
                    analysis_df['Écart_Prix'] > 0.5, 'Surévaluée (Vente)',
                    np.where(analysis_df['Écart_Prix'] < -0.5, 'Sous-évaluée (Achat)', 'Juste Valeur')
                )
                
                st.success("Analyse des opportunités terminée!")
                
                st.subheader("Résultats de l'Analyse")
                
                # Mise en forme pour l'affichage
                display_df = analysis_df.copy()
                display_df.rename(columns={
                    'Prix_Actuel': 'Prix de Marché (€)',
                    'Prix_Théorique': 'Prix Théorique (€)',
                    'Écart_Prix': 'Écart (€)',
                    'YTM_Reference (%)': 'YTM Réf. (%)'
                }, inplace=True)
                
                st.dataframe(
                    display_df[['ISIN', 'Prix de Marché (€)', 'Prix Théorique (€)', 'Écart (€)', 'Opportunité']],
                    hide_index=True
                )
                
                # Affichage des opportunités
                opportunities = display_df[display_df['Opportunité'] != 'Juste Valeur']
                
                if not opportunities.empty:
                    st.markdown("### Opportunités Identifiées")
                    for index, row in opportunities.iterrows():
                        if row['Opportunité'] == 'Sous-évaluée (Achat)':
                            st.success(f"**Achat :** L'obligation {row['ISIN']} est sous-évaluée. Prix de Marché: {row['Prix de Marché (€)']:.2f} €, Prix Théorique: {row['Prix Théorique (€)']:.2f} € (Écart: {row['Écart (€)']:.2f} €)")
                        else:
                            st.error(f"**Vente :** L'obligation {row['ISIN']} est surévaluée. Prix de Marché: {row['Prix de Marché (€)']:.2f} €, Prix Théorique: {row['Prix Théorique (€)']:.2f} € (Écart: {row['Écart (€)']:.2f} €)")
                else:
                    st.info("Aucune opportunité d'arbitrage significative identifiée (Écart > 0.5 €).")
                
        except Exception as e:
            st.error(f"Une erreur est survenue lors de la recherche d'opportunités : {e}")
            st.exception(e)
