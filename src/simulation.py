import numpy
import pandas

from config import simulations, inflation_mean, inflation_volatility
from mortality import sample_death_age
from portfolio import sample_portfolio_return
from utils import format

def run_simulation():
    retire_savings = int(input("Starting savings: "))
    retire_withdrawal = int(input("Yearly withdrawal: "))
    retire_age = int(input("Retirement age: "))
    stock_share = int(input("Stock percentage of portfolio (rest will be bonds): ")) / 100
    bond_share = 1 - stock_share

    wealth_paths = numpy.full((simulations, 110 - retire_age + 1), numpy.nan)
    rows = []

    for i in range(0, simulations):
        age = retire_age
        savings = retire_savings
        withdrawal = retire_withdrawal

        death_age = sample_death_age(age)
        ruined = False
        ruin_age = None

        while (age < death_age):
            wealth_paths[i, age - retire_age] = savings
            # Keeping track of yearly wealth for all simulations

            savings -= withdrawal / 2
            # Half withdrawal, simulating a mid year withdrawal
            savings *= sample_portfolio_return(stock_share, bond_share)
            savings -= withdrawal / 2

            if (savings <= 0):
                savings = 0
                ruined = True
                ruin_age = age
                wealth_paths[i, age - retire_age] = 0
                break
                # When in ruin, end
            
            inflation = numpy.random.normal(0.02, 0.01)
            withdrawal *= (1 + inflation)
            age += 1
            # Otherwise, keep simulating
        
        rows.append({
            "final_savings": int(savings),
            "death_age": death_age,
            "ruined": ruined,
            "ruin_age": ruin_age
        })

    results_df = pandas.DataFrame(rows)
    print_results(results_df)

def print_results(df):
    print("\nTotal simulations:", format(simulations))
    print("\nHighest savings:", format(df['final_savings'].max()) + "$")
    print("Median savings:", format(df['final_savings'].median()) + "$")
    print("\nHighest age:", df["death_age"].max())
    print("Median age at death:", df["death_age"].median())
    print("\nChance of ruin:", str(df["ruined"].sum() / len(df) * 100) + "%")
    print("Median age of ruin:", str(df["ruin_age"].median()))

if __name__ == "__main__":
    run_simulation()