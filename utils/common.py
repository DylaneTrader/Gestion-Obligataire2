# app/utils/common.py

import streamlit as st
import pandas as pd

def set_page_config():
    """
    Configure les paramètres de base de la page Streamlit.
    """
    st.set_page_config(
        page_title="Gestion Obligataire",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_data(file_path):
    """
    Charge un fichier de données (CSV ou Excel) en DataFrame.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            st.error("Format de fichier non supporté. Veuillez utiliser CSV ou Excel.")
            return None
        return df
    except FileNotFoundError:
        st.error(f"Fichier non trouvé: {file_path}")
        return None
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier: {e}")
        return None

def display_header(title, icon):
    """
    Affiche un en-tête stylisé pour la page.
    """
    st.markdown(f"""
        <style>
            .stApp {{
                background-color: #f0f2f6;
            }}
            .header-style {{
                font-size: 2.5em;
                font-weight: bold;
                color: #0e1117;
                padding-bottom: 10px;
                border-bottom: 2px solid #0e1117;
                margin-bottom: 20px;
            }}
        </style>
        <div class="header-style">{icon} {title}</div>
    """, unsafe_allow_html=True)

# Exemple de données pour les obligations
BOND_EXAMPLE_DATA = {
    'ISIN': ['FR0010000001', 'US9128285H31', 'DE0001102381'],
    'Nominal': [1000, 1000, 1000],
    'Taux_Coupon': [0.03, 0.05, 0.015],
    'Frequence_Coupon': [1, 2, 1], # 1: Annuel, 2: Semestriel
    'Maturite_Annees': [5, 10, 3],
    'Prix_Actuel': [1015.50, 980.00, 1005.25]
}

def get_bond_example_df():
    """
    Retourne un DataFrame d'exemple pour les obligations.
    """
    return pd.DataFrame(BOND_EXAMPLE_DATA)
