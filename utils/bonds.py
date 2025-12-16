# app/utils/bonds.py

import numpy as np
from datetime import date, timedelta

def calculate_ytm(price, face_value, coupon_rate, frequency, years_to_maturity):
    """
    Calcule le rendement à l'échéance (YTM) d'une obligation.
    Utilise une méthode itérative (Newton-Raphson) ou une approximation.
    Pour la simplicité, nous utiliserons une approximation ici.
    """
    # Approximation du YTM
    annual_coupon = face_value * coupon_rate
    
    # Rendement approximatif (Yield Approximation)
    # YTM ≈ (C + (FV - P) / n) / ((FV + P) / 2)
    # Où:
    # C = Paiement de coupon annuel
    # FV = Valeur nominale
    # P = Prix actuel
    # n = Nombre d'années jusqu'à l'échéance
    
    ytm_approx = (annual_coupon + (face_value - price) / years_to_maturity) / ((face_value + price) / 2)
    
    # Pour un calcul plus précis, une boucle ou une fonction scipy.optimize.newton serait nécessaire.
    # Nous allons retourner l'approximation pour l'instant.
    return ytm_approx

def calculate_price(ytm, face_value, coupon_rate, frequency, years_to_maturity):
    """
    Calcule le prix d'une obligation.
    """
    if ytm == 0:
        return face_value + (coupon_rate * face_value * years_to_maturity)
        
    periods = years_to_maturity * frequency
    coupon_payment = (coupon_rate / frequency) * face_value
    rate_per_period = ytm / frequency
    
    # Prix = Somme des valeurs actuelles des coupons + Valeur actuelle du principal
    price = 0
    for t in range(1, int(periods) + 1):
        price += coupon_payment / (1 + rate_per_period)**t
        
    price += face_value / (1 + rate_per_period)**periods
    
    return price

def calculate_duration(price, face_value, coupon_rate, frequency, years_to_maturity, ytm=None):
    """
    Calcule la Duration de Macaulay.
    """
    if ytm is None:
        ytm = calculate_ytm(price, face_value, coupon_rate, frequency, years_to_maturity)
        
    periods = years_to_maturity * frequency
    coupon_payment = (coupon_rate / frequency) * face_value
    rate_per_period = ytm / frequency
    
    weighted_sum = 0
    pv_sum = 0
    
    for t in range(1, int(periods) + 1):
        cash_flow = coupon_payment
        if t == periods:
            cash_flow += face_value
            
        pv = cash_flow / (1 + rate_per_period)**t
        weighted_sum += t * pv
        pv_sum += pv
        
    # Si le prix est fourni, on utilise le prix comme pv_sum pour plus de cohérence
    # Sinon, on utilise la somme des PV calculées
    if price is not None and price > 0:
        macaulay_duration = weighted_sum / price
    else:
        macaulay_duration = weighted_sum / pv_sum
        
    # La duration de Macaulay est en périodes. On la convertit en années.
    macaulay_duration_years = macaulay_duration / frequency
    
    # Duration Modifiée = Duration de Macaulay / (1 + YTM/frequency)
    modified_duration = macaulay_duration_years / (1 + rate_per_period)
    
    return macaulay_duration_years, modified_duration

# Exemple d'utilisation (pour test)
if __name__ == '__main__':
    # Obligation avec 5% de coupon, valeur nominale 1000, 5 ans, paiement annuel (frequency=1)
    # Prix actuel 950
    price = 950
    face_value = 1000
    coupon_rate = 0.05
    frequency = 1
    years_to_maturity = 5
    
    ytm = calculate_ytm(price, face_value, coupon_rate, frequency, years_to_maturity)
    print(f"YTM approximatif: {ytm:.4f}")
    
    price_calc = calculate_price(ytm, face_value, coupon_rate, frequency, years_to_maturity)
    print(f"Prix calculé avec YTM: {price_calc:.2f}")
    
    macaulay, modified = calculate_duration(price, face_value, coupon_rate, frequency, years_to_maturity, ytm)
    print(f"Duration de Macaulay (années): {macaulay:.4f}")
    print(f"Duration Modifiée (années): {modified:.4f}")
