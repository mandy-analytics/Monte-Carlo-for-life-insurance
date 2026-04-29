import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION & ASSUMPTIONS ---
NUM_SIMULATIONS = 100000
START_AGE = 35
TERM_YEARS = 20
BENEFIT_AMOUNT = 250000
INTEREST_RATE = 0.04  # Annual Effective Rate
EXPENSE_LOADING = 0.15 # 15% markup for admin/profit

def generate_mortality_table(base_age=0, max_age=120):
    """
    Simulates a Gompertz-Makeham mortality law curve.
    In a real project, replace this by loading a CSV (e.g., VBT 2015 Table).
    """
    ages = np.arange(base_age, max_age + 1)
    # qx = probability of death. Typical actuarial curve:
    qx = 0.0001 + 0.00005 * 1.09**ages 
    qx = np.clip(qx, 0, 1) # Ensure prob doesn't exceed 1
    return pd.DataFrame({'age': ages, 'qx': qx})

def run_monte_carlo():
    # 1. Load Data
    df_mort = generate_mortality_table()
    relevant_qx = df_mort.loc[(df_mort['age'] >= START_AGE) & 
                              (df_mort['age'] < START_AGE + TERM_YEARS), 'qx'].values
    
    # 2. Probability Calculations
    # Probability of surviving to the start of each year
    px = 1 - relevant_qx
    survival_probs = np.concatenate(([1.0], np.cumprod(px)[:-1]))
    # Probability of dying in each specific year (t|qx)
    prob_death_in_year = survival_probs * relevant_qx
    
    # 3. Vectorized Simulation
    # Each random draw represents a policyholder's life path
    draws = np.random.uniform(0, 1, NUM_SIMULATIONS)
    cdf_death = np.cumsum(prob_death_in_year)
    
    # Find which year death occurs. searchsorted finds the first index where 
    # the CDF exceeds our random draw.
    death_years = np.searchsorted(cdf_death, draws)
    
    # 4. Financial Modeling (Present Value)
    # Boolean mask: did they die during the term?
    died_in_term = death_years < TERM_YEARS
    
    # Calculate PV of the Benefit (Paid at end of year of death)
    discount_factors = 1 / (1 + INTEREST_RATE)**(death_years + 1)
    pv_benefits = np.where(died_in_term, BENEFIT_AMOUNT * discount_factors, 0)
    
    # Calculate Net Single Premium (NSP)
    nsp = np.mean(pv_benefits)
    loaded_premium = nsp * (1 + EXPENSE_LOADING)
    
    return pv_benefits, nsp, loaded_premium

# --- EXECUTION & VISUALIZATION ---
if __name__ == "__main__":
    pvs, nsp, final_price = run_monte_carlo()
    
    print("-" * 30)
    print(f"ACTUARIAL RESULTS (Age {START_AGE}, {TERM_YEARS}-Year Term)")
    print(f"Net Single Premium: ${nsp:,.2f}")
    print(f"Final Price (with {EXPENSE_LOADING*100}% loading): ${final_price:,.2f}")
    print("-" * 30)

    # Plotting for Spyder's Plot Pane
    plt.figure(figsize=(10, 6))
    plt.hist(pvs[pvs > 0], bins=50, alpha=0.7, color='#2ca02c', edgecolor='black')
    plt.axvline(nsp, color='red', linestyle='dashed', linewidth=2, label=f'Mean (NSP): ${nsp:.2f}')
    plt.title(f"Distribution of Claims: ${BENEFIT_AMOUNT:,} Term Life")
    plt.xlabel("Present Value of Payout ($)")
    plt.ylabel("Number of Simulated Lives")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.show()