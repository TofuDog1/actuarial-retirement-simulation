import numpy
import matplotlib.pyplot as matplot

from config import simulations

def generate_graphs(results_df, wealth_paths_df, retire_age):
    graph_life_ex(results_df['death_age'])
    graph_ruin_age(results_df['ruin_age'])
    graph_ruin_chance(results_df['ruin_age'], retire_age)
    graph_final_money(results_df['final_savings'])
    graph_wealth_paths(wealth_paths_df)
    graph_wealth_paths_cone(wealth_paths_df)
    graph_simulations(wealth_paths_df)

def graph_life_ex(df):
    matplot.title("Life Expectancy Distribution")
    matplot.xlabel("Age")
    matplot.ylabel("Amount of People")

    matplot.hist(df, bins='auto', histtype='stepfilled')
    matplot.savefig("outputs/life_expectancy_distribution.png")
    matplot.close()

def graph_ruin_age(df):
    df = df.dropna().astype(int)

    matplot.title("Age at Which Portfolio Is Depleted")
    matplot.xlabel("Age")
    matplot.ylabel("Number of Simulations")

    if not df.empty:
        # One bar for each possible ruin age
        ages = numpy.arange(df.min(), df.max() + 1)
        counts = df.value_counts().reindex(ages, fill_value=0)

        matplot.bar(
            ages,
            counts,
            width=0.8,
            label="Simulations ruined"
        )

        matplot.legend()

    matplot.tight_layout()
    matplot.savefig("outputs/ruin_age_distribution.png")
    matplot.close()

def graph_ruin_chance(df, retire_age):
    df = df.dropna().astype(int)

    matplot.title("Cumulative Probability of Portfolio Ruin")
    matplot.xlabel("Years in Retirement")
    matplot.ylabel("Probability of Ruin (%)")
    matplot.ylim(0, 100)

    if not df.empty:
        # Convert ruin ages to years since retirement
        ruin_years = df - retire_age

        # Count how many simulations ruin at each year
        years = numpy.arange(
            ruin_years.min(),
            ruin_years.max() + 1
        )

        counts = ruin_years.value_counts().reindex(
            years,
            fill_value=0
        )

        # Cumulative number of ruined simulations
        cumulative = counts.cumsum()

        # Convert to percentage of all simulations
        cumulative_percent = cumulative / simulations * 100

        matplot.step(
            years,
            cumulative_percent,
            where="post",
            linewidth=2,
            label="Cumulative ruin probability"
        )

        matplot.fill_between(
            years,
            cumulative_percent,
            step="post",
            alpha=0.2
        )

        matplot.legend()

    matplot.tight_layout()
    matplot.savefig("outputs/cumulative_ruin_chance.png")
    matplot.close()

def graph_final_money(df):
    data = df[df > 0]
    logdata = numpy.log10(data)

    matplot.title("Money Distribution at Death Among Non-Ruined Retirees")
    matplot.xlabel("Ending Wealth in Dollars")
    matplot.ylabel("Amount of People")
    matplot.hist(logdata, bins='auto', histtype='stepfilled')

    ticks = matplot.xticks()[0]
    matplot.xticks(ticks, [f"${10**t:,.0f}" for t in ticks], rotation=45)
    matplot.tick_params(labelsize=7)

    matplot.tight_layout()
    matplot.savefig("outputs/money_distribution.png")
    matplot.close()

def graph_wealth_paths(df):
    years = numpy.arange(df.shape[1])

    p10 = df.quantile(0.1, axis=0)
    p25 = df.quantile(0.25, axis=0)
    p50 = df.quantile(0.50, axis=0)
    p75 = df.quantile(0.75, axis=0)
    p90 = df.quantile(0.9, axis=0)
    p99 = df.quantile(0.99, axis=0)

    matplot.title("Percentile Wealth by Year")
    matplot.xlabel("Years in Retirement")
    matplot.ylabel("Wealth in Dollars")

    matplot.plot(years, p10, label="10th percentile")
    matplot.plot(years, p25, label="25th percentile")
    matplot.plot(years, p50, label="50th percentile (median)", linewidth=2)
    matplot.plot(years, p75, label="75th percentile")
    matplot.plot(years, p90, label="90th percentile")
    matplot.plot(years, p99, label="99th percentile")

    matplot.legend()
    matplot.grid()

    matplot.tight_layout()
    matplot.savefig("outputs/wealth_paths.png")
    matplot.close()

def graph_wealth_paths_cone(df):
    years = numpy.arange(df.shape[1])

    p10 = df.quantile(0.1, axis=0)
    p25 = df.quantile(0.25, axis=0)
    p40 = df.quantile(0.40, axis=0)
    p50 = df.quantile(0.50, axis=0)
    p60 = df.quantile(0.60, axis=0)
    p75 = df.quantile(0.75, axis=0)
    p90 = df.quantile(0.9, axis=0)
    p99 = df.quantile(0.99, axis=0)

    matplot.title("Wealth Distribution Over Retirement")
    matplot.xlabel("Years in Retirement")
    matplot.ylabel("Wealth in Dollars")

    # 10th–90th percentile region
    matplot.fill_between(years, p10, p90, alpha=0.25, label="10th–90th percentile")
    # 25th–75th percentile region
    matplot.fill_between(years, p25, p75, alpha=0.35, label="25th–75th percentile")
    # 40th–60th percentile region
    matplot.fill_between(years, p40, p60, alpha=0.5, label="40th–60th percentile")
    # Median
    matplot.plot(years, p50, linewidth=2, label="Median")
    # 99th percentile
    matplot.plot(years, p99, linestyle="--", label="99th percentile")

    matplot.legend()
    matplot.grid()
    matplot.tight_layout()
    matplot.savefig(
        "outputs/wealth_cone.png"
    )

    matplot.close()

def graph_simulations(df):
    number_of_paths = min(1000, len(df))

    selected = numpy.random.choice(
        len(df),
        size=number_of_paths,
        replace=False
    )

    years = numpy.arange(df.shape[1])

    matplot.title("Individual Simulated Wealth Paths")
    matplot.xlabel("Years in Retirement")
    matplot.ylabel("Wealth in Dollars")

    for i in selected:
        matplot.plot(
            years,
            df.iloc[i],
            alpha=0.25
        )

    median = df.median(axis=0)

    matplot.plot(
        years,
        median,
        linewidth=2,
        label="Median"
    )

    matplot.legend()
    matplot.grid()
    matplot.tight_layout()
    matplot.savefig(
        "outputs/individual_wealth_paths.png"
    )

    matplot.close()