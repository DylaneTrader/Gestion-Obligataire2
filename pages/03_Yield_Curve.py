# app/pages/03_Yield_Curve.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.common import set_page_config, display_header
from utils.yields import create_dummy_yield_curve, interpolate_yield_curve

set_page_config()
display_header("Analyse de la Courbe de Rendement (Yield Curve)", "📊")

st.markdown("""
    Cette page permet de visualiser et d'analyser la **courbe de rendement**.
    Vous pouvez charger vos propres données ou utiliser des données d'exemple.
""")

# --- Saisie des données ---
st.subheader("Données de la Courbe de Rendement")

# Option de chargement de fichier ou d'utilisation de données d'exemple
data_source = st.radio(
    "Source des données",
    ("Données d'Exemple", "Charger un Fichier (CSV/Excel)"),
    index=0
)

curve_df = None
if data_source == "Données d'Exemple":
    curve_df = create_dummy_yield_curve(None)
    st.dataframe(curve_df, hide_index=True)
else:
    uploaded_file = st.file_uploader("Choisissez un fichier CSV ou Excel", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                curve_df = pd.read_csv(uploaded_file)
            else:
                curve_df = pd.read_excel(uploaded_file)
            
            st.success("Fichier chargé avec succès!")
            st.dataframe(curve_df.head(), hide_index=True)
            
            # Vérification des colonnes
            if 'Maturity' not in curve_df.columns or 'Yield' not in curve_df.columns:
                st.error("Le fichier doit contenir les colonnes 'Maturity' (en années) et 'Yield' (en %).")
                curve_df = None
                
        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")

# --- Visualisation et Interpolation ---
if curve_df is not None:
    st.subheader("Visualisation et Interpolation")
    
    # Paramètres d'interpolation
    max_maturity = curve_df['Maturity'].max()
    target_maturities = np.linspace(curve_df['Maturity'].min(), max_maturity, 100)
    
    # Interpolation
    interpolated_df = interpolate_yield_curve(curve_df, target_maturities)
    
    # Préparation des données pour le graphique
    plot_df = pd.DataFrame({
        'Maturity': pd.concat([curve_df['Maturity'], interpolated_df['Maturity']]),
        'Yield': pd.concat([curve_df['Yield'], interpolated_df['Yield']]),
        'Type': ['Points de Données'] * len(curve_df) + ['Courbe Interpolée'] * len(interpolated_df)
    })
    
    # Création du graphique interactif avec Plotly
    fig = px.line(
        plot_df[plot_df['Type'] == 'Courbe Interpolée'],
        x='Maturity',
        y='Yield',
        title='Courbe de Rendement Interpolée',
        labels={'Maturity': 'Maturité (Années)', 'Yield': 'Rendement (%)'}
    )
    
    # Ajouter les points de données originaux
    fig.add_scatter(
        x=curve_df['Maturity'],
        y=curve_df['Yield'],
        mode='markers',
        name='Points de Données',
        marker=dict(size=8, color='red')
    )
    
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    # --- Analyse de la Pente ---
    st.subheader("Analyse de la Pente")
    
    # Calcul de l'écart de rendement (Spread)
    short_term_maturity = st.selectbox("Maturité Court Terme (Années)", sorted(curve_df['Maturity'].unique()), index=0)
    long_term_maturity = st.selectbox("Maturité Long Terme (Années)", sorted(curve_df['Maturity'].unique()), index=len(curve_df)-1)
    
    short_yield = curve_df[curve_df['Maturity'] == short_term_maturity]['Yield'].iloc[0]
    long_yield = curve_df[curve_df['Maturity'] == long_term_maturity]['Yield'].iloc[0]
    
    spread = long_yield - short_yield
    
    st.metric(f"Écart de Rendement ({long_term_maturity}a - {short_term_maturity}a)", f"{spread:.2f} %")
    
    if spread > 0.5:
        st.success("Pente Positive (Normale) : Indique généralement une croissance économique attendue.")
    elif spread < -0.5:
        st.error("Pente Négative (Inversée) : Peut signaler une récession économique future.")
    else:
        st.warning("Pente Plate : Incertitude économique ou transition.")
