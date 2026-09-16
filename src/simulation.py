import numpy
import pandas

from config import simulations, inflation_mean, inflation_volatility
from mortality import sample_death_age
from portfolio import sample_portfolio_return
from utils import format
from graphs import generate_graphs

def run_simulation():
    retire_savings = int(input("\nStarting savings: "))
    retire_withdrawal = int(input("Yearly withdrawal: "))
    retire_age = int(input("Retirement age: "))
    stock_share = int(input("Stock percentage of portfolio (rest will be bonds): ")) / 100
    bond_share = 1 - stock_share

    wealth_paths = numpy.full((simulations, 110 - retire_age + 1), numpy.nan)
    rows = []

    for i in range(simulations):
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
            # Second half of withdrawal

            if (savings <= 0):
                savings = 0
                ruined = True
                ruin_age = age
                wealth_paths[i, age - retire_age : death_age - retire_age] = 0
                break
                # When in ruin, end
            
            inflation = numpy.random.normal(inflation_mean, inflation_volatility)
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
    wealth_paths_df = pandas.DataFrame(wealth_paths)
    print_results(results_df)
    generate_graphs(results_df, wealth_paths_df, retire_age)

def print_results(df):
    print("\nTotal simulations:", format(simulations))
    
    print("\nLongevity")
    print("---------")
    print("Highest age:", df["death_age"].max())
    print("Median age at death:", df["death_age"].median())

    print("\nWealth Outcomes")
    print("---------------")
    print("Highest savings: $" + format(df['final_savings'].max()))
    print("Median savings: $" + format(df['final_savings'].median()))
    
    print("\nFinal Wealth Distribution")
    print("-------------------")
    print("10th percentile: $" + format(df['final_savings'].quantile(0.1)))
    print("25th: $" + format(df['final_savings'].quantile(0.25)))
    print("50th: $" + format(df['final_savings'].quantile(0.5)))
    print("75th: $" + format(df['final_savings'].quantile(0.75)))
    print("90th: $" + format(df['final_savings'].quantile(0.9)))
    print("99th: $" + format(df['final_savings'].quantile(0.99)))

    print("\nRisk")
    print("----")
    print("Chance of ruin:", str(round(df["ruined"].sum() / len(df) * 100, 3)) + "%")

    ruin_ages = df.loc[df["ruined"], "ruin_age"]

    if not ruin_ages.empty:
        print("Median age of ruin:", ruin_ages.median())
    else:
        print("Median age of ruin: N/A")

    print("")