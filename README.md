# Canadian Retirement Monte Carlo Simulator

A Python-based Monte Carlo simulation for analyzing retirement portfolio outcomes under uncertainty.

The simulator runs 100,000 possible retirement scenarios by randomly varying mortality, investment returns, and inflation. It then analyzes the resulting wealth paths and probability of portfolio ruin.

## Features

- Canadian mortality modeling using Statistics Canada mortality data
- Stochastic investment returns using lognormal distributions
- Adjustable stock/bond portfolio allocation
- Inflation shocks
- Monte Carlo simulation with 100,000 scenarios
- Portfolio ruin probability
- Distribution of wealth at the end of each simulation
- Median and percentile wealth paths
- Individual simulated wealth paths
- Wealth distribution fan chart
- Ruin-age distribution
- Cumulative probability of portfolio ruin

## Model

Each simulation represents one possible retirement outcome.

At the beginning of retirement, the user specifies:

- Starting portfolio value
- Annual withdrawal amount
- Retirement age
- Percentage allocated to stocks

The remaining portfolio is allocated to bonds.

Each year, the simulation:

1. Samples a death age using official Canadian mortality probabilities.
2. Withdraws half of the annual spending amount.
3. Applies a randomly generated portfolio return.
4. Withdraws the remaining half of the annual spending amount.
5. Adjusts the following year's withdrawal for inflation.
6. Checks whether the portfolio has been depleted.
7. Repeats until death or portfolio ruin.

The simulation is repeated 100,000 times to produce a distribution of possible outcomes.

## Investment Model

Stock and bond returns are modeled using lognormal distributions.

The current assumptions are based on long-term capital market projections:

| Asset | Expected Return | Volatility |
|-------|-----------------|------------|
| Stocks | 6.6% | 12.7% |
| Bonds | 3.4% | 5.8% |

The user can specify the percentage of the portfolio invested in stocks, with the remainder invested in bonds.

## Inflation

Inflation is modeled as a normally distributed annual shock with:

- Mean: 2.0%
- Volatility: 1.0%

Annual withdrawals are adjusted according to the simulated inflation rate.

## Mortality

The simulation uses age-specific mortality probabilities (`qx`) from a Canadian life table.

For each simulated retirement:

Retirement age\
      ↓\
Sample annual mortality probability\
      ↓\
Determine simulated age at death\
      ↓\
Simulate portfolio until death or ruin\


The mortality data is stored in:\
data/life_table.csv

## Outputs

The simulation generates several graphs in the outputs/ directory:

life_expectancy_distribution.png\
Distribution of simulated ages at death

ruin_age_distribution.png\
Ages at which portfolios are depleted

cumulative_ruin_chance.png\
Cumulative probability of portfolio ruin over retirement

money_distribution.png\
Distribution of ending wealth among non-ruined simulations

wealth_paths.png\
Wealth percentiles over time

wealth_cone.png\
Fan chart showing the distribution of simulated wealth

individual_wealth_paths.png\
Individual simulated wealth trajectories

## Project Structure
retirement_simulator/\
├── src/\
│   ├── main.py\
│   ├── simulation.py\
│   ├── portfolio.py\
│   ├── mortality.py\
│   ├── graphs.py\
│   ├── config.py\
│   └── utils.py\
├── data/\
│   └── life_table.csv\
├── outputs/\
├── .gitignore\
└── README.md\

## Installation

Clone the repository and install the required Python packages:

pip install numpy pandas matplotlib

## Running the Simulation

From the project directory:

python src/main.py

The program will prompt for:

Starting savings:\
Yearly withdrawal:\
Retirement age:\
Stock percentage of portfolio:\

After the simulation finishes, summary statistics will be printed to the terminal and graphs will be saved to outputs/.

## Example

A simulation might be configured with:

Starting savings: 1000000\
Yearly withdrawal: 40000\
Retirement age: 65\
Stock percentage of portfolio: 60\

The simulator then generates 100,000 possible retirement paths using the specified assumptions.

## Limitations

This simulation is intended as a modeling and educational project rather than financial advice.

The current model does not account for several factors that can materially affect retirement outcomes, including:

Taxes\
CPP and OAS\
Investment fees\
Individual security selection\
Stock/bond return correlation\
Changes in asset allocation over time\
Variable spending strategies\
Healthcare expenses\
Housing costs\
Government policy changes\
Sequence-of-returns effects beyond the modeled stochastic returns\

The results are therefore dependent on the assumptions and distributions used by the model.

## Data Sources

Mortality\
Statistics Canada mortality/life table data.

Expected Returns\
FP Canada, 2025 Projection Assumption Guidelines.

Volatility\
CIBC, Long-Term Annualized Capital Market Report, 2025.

## Disclaimer

This project is for educational and research purposes only. It is not financial advice, and simulated outcomes should not be interpreted as predictions of actual future investment performance.