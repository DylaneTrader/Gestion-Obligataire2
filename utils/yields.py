# app/utils/yields.py

import pandas as pd
import numpy as np
from scipy.interpolate import CubicSpline

def create_dummy_yield_curve(maturities):
    """
    Crée une courbe de rendement factice pour la démonstration.
    """
    # Exemple de données pour une courbe normale (pente positive)
    # Maturités en années
    # Rendements en pourcentage
    yields_data = {
        0.5: 1.5,
        1.0: 1.8,
        2.0: 2.2,
        3.0: 2.5,
        5.0: 3.0,
        7.0: 3.3,
        10.0: 3.5,
        20.0: 3.8,
        30.0: 4.0
    }
    
    # Créer un DataFrame pour la courbe de rendement
    curve_df = pd.DataFrame(list(yields_data.items()), columns=['Maturity', 'Yield'])
    
    return curve_df

def interpolate_yield_curve(curve_df, target_maturities):
    """
    Interpole la courbe de rendement en utilisant la méthode des splines cubiques.
    
    Args:
        curve_df (pd.DataFrame): DataFrame avec les colonnes 'Maturity' et 'Yield'.
        target_maturities (list): Liste des maturités cibles pour l'interpolation.
        
    Returns:
        pd.DataFrame: DataFrame avec les maturités cibles et les rendements interpolés.
    """
    # Convertir les rendements en décimal pour l'interpolation
    x = curve_df['Maturity'].values
    y = curve_df['Yield'].values / 100
    
    # Utiliser les splines cubiques pour l'interpolation
    cs = CubicSpline(x, y)
    
    # Calculer les rendements interpolés
    interpolated_yields = cs(target_maturities) * 100
    
    # Créer le DataFrame de résultats
    interpolated_df = pd.DataFrame({
        'Maturity': target_maturities,
        'Yield': interpolated_yields
    })
    
    return interpolated_df

# Exemple d'utilisation (pour test)
if __name__ == '__main__':
    maturities = [0.5, 1, 2, 3, 5, 7, 10, 20, 30]
    curve_df = create_dummy_yield_curve(maturities)
    print("Courbe de rendement initiale:")
    print(curve_df)
    
    target_maturities = np.linspace(0.5, 30, 60)
    interpolated_df = interpolate_yield_curve(curve_df, target_maturities)
    print("\nCourbe de rendement interpolée (premières lignes):")
    print(interpolated_df.head())
