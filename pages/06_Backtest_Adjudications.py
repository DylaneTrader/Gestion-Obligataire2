# app/pages/06_Backtest_Adjudications.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.common import set_page_config, display_header

set_page_config()
display_header("Backtest de Stratégies d'Adjudication", "⏳")

st.markdown("""
    Évaluez la performance historique de vos stratégies de soumission aux adjudications.
    
    **Note :** Cette page est une maquette. Pour un backtest réel, une base de données
    historique des soumissions et des résultats d'adjudication serait nécessaire.
""")

# --- Données de Backtest Factices ---
@st.cache_data
def load_backtest_data():
    dates = pd.to_datetime(pd.date_range(start='2022-01-01', periods=12, freq='M'))
    data = {
        'Date': dates,
        'Prix_Marginal_Réel': np.random.uniform(98.0, 102.0, 12),
        'Prix_Soumis': np.random.uniform(97.5, 101.5, 12),
        'Montant_Soumis': np.random.randint(50, 200, 12),
        'Montant_Alloué': np.random.randint(0, 200, 12)
    }
    df = pd.DataFrame(data)
    # Simuler l'allocation
    df['Allocation_Ratio'] = np.where(df['Prix_Soumis'] >= df['Prix_Marginal_Réel'], 
                                     df['Montant_Alloué'] / df['Montant_Soumis'], 
                                     0)
    df['Allocation_Ratio'] = df['Allocation_Ratio'].clip(upper=1.0)
    df['Montant_Alloué'] = df['Montant_Soumis'] * df['Allocation_Ratio']
    
    # Simuler le gain/perte (très simplifié)
    df['Performance'] = (df['Prix_Marginal_Réel'] - df['Prix_Soumis']) * df['Montant_Alloué']
    
    return df

backtest_df = load_backtest_data()

# --- Affichage des Résultats ---
st.subheader("Historique des Adjudications Simulé")
st.dataframe(backtest_df.style.format({
    'Prix_Marginal_Réel': "{:.2f}",
    'Prix_Soumis': "{:.2f}",
    'Montant_Soumis': "{:,.0f}",
    'Montant_Alloué': "{:,.0f}",
    'Allocation_Ratio': "{:.1%}",
    'Performance': "{:,.2f}"
}), hide_index=True)

# --- Visualisation de la Performance ---
st.subheader("Visualisation de la Performance")

# Graphique de l'écart de prix
fig_price = px.line(
    backtest_df,
    x='Date',
    y=['Prix_Marginal_Réel', 'Prix_Soumis'],
    title='Comparaison Prix Soumis vs Prix Marginal Réel',
    labels={'value': 'Prix (%)', 'variable': 'Type de Prix'}
)
fig_price.update_layout(hovermode="x unified")
st.plotly_chart(fig_price, use_container_width=True)

# Graphique de la performance
fig_perf = px.bar(
    backtest_df,
    x='Date',
    y='Performance',
    title='Performance par Adjudication (Gain/Perte Simulé)',
    labels={'Performance': 'Performance (€)'}
)
st.plotly_chart(fig_perf, use_container_width=True)

# --- Métriques Clés ---
st.subheader("Métriques de Backtest")

total_performance = backtest_df['Performance'].sum()
avg_allocation = backtest_df['Allocation_Ratio'].mean()
hit_rate = (backtest_df['Allocation_Ratio'] > 0).sum() / len(backtest_df)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Performance Totale Simulé", f"{total_performance:,.2f} €")
with col2:
    st.metric("Ratio d'Allocation Moyen", f"{avg_allocation:.1%}")
with col3:
    st.metric("Taux de Succès (Hit Rate)", f"{hit_rate:.1%}")

st.markdown("""
    <div style="margin-top: 20px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
        **Conclusion :** L'analyse montre comment les prix soumis se sont comparés
        au prix marginal réel, impactant le ratio d'allocation et la performance simulée.
    </div>
""", unsafe_allow_html=True)
