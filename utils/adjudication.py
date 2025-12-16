# app/utils/adjudication.py

import pandas as pd

def calculate_marginal_price(bids_df, total_amount):
    """
    Calcule le prix marginal et les allocations dans une adjudication à prix multiple.
    
    Args:
        bids_df (pd.DataFrame): DataFrame avec les colonnes 'Price' et 'Amount'.
        total_amount (float): Montant total de l'obligation à allouer.
        
    Returns:
        tuple: (marginal_price, allocated_bids_df)
    """
    # 1. Trier les soumissions par prix décroissant
    bids_df = bids_df.sort_values(by='Price', ascending=False).reset_index(drop=True)
    
    # 2. Calculer le montant cumulé
    bids_df['Cumulative_Amount'] = bids_df['Amount'].cumsum()
    
    # 3. Trouver le prix marginal
    # Le prix marginal est le prix de la soumission qui fait dépasser le montant total.
    marginal_row = bids_df[bids_df['Cumulative_Amount'] >= total_amount].iloc[0]
    marginal_price = marginal_row['Price']
    
    # 4. Allouer les soumissions au-dessus du prix marginal
    allocated_bids = bids_df[bids_df['Price'] > marginal_price].copy()
    allocated_bids['Allocation'] = allocated_bids['Amount']
    
    # 5. Calculer l'allocation pour le prix marginal
    amount_allocated_above = allocated_bids['Allocation'].sum()
    remaining_amount = total_amount - amount_allocated_above
    
    marginal_bids = bids_df[bids_df['Price'] == marginal_price].copy()
    total_marginal_amount = marginal_bids['Amount'].sum()
    
    if total_marginal_amount > 0:
        allocation_ratio = remaining_amount / total_marginal_amount
        marginal_bids['Allocation'] = marginal_bids['Amount'] * allocation_ratio
    else:
        # Cas où le prix marginal est le plus bas et il n'y a pas de soumission à ce prix
        marginal_bids['Allocation'] = 0
        
    # 6. Combiner les allocations
    final_allocations = pd.concat([allocated_bids, marginal_bids])
    
    # 7. Les soumissions en dessous du prix marginal n'ont pas d'allocation
    unallocated_bids = bids_df[bids_df['Price'] < marginal_price].copy()
    unallocated_bids['Allocation'] = 0
    
    final_allocations = pd.concat([final_allocations, unallocated_bids]).sort_values(by='Price', ascending=False)
    
    return marginal_price, final_allocations

# Exemple d'utilisation (pour test)
if __name__ == '__main__':
    data = {
        'Price': [99.50, 99.45, 99.40, 99.35, 99.30],
        'Amount': [100, 150, 200, 100, 50]
    }
    bids_df = pd.DataFrame(data)
    total_amount = 400
    
    marginal_price, allocations = calculate_marginal_price(bids_df, total_amount)
    
    print(f"Montant total à allouer: {total_amount}")
    print(f"Prix Marginal: {marginal_price}")
    print("\nAllocations:")
    print(allocations)
    print(f"\nTotal alloué: {allocations['Allocation'].sum():.2f}")
