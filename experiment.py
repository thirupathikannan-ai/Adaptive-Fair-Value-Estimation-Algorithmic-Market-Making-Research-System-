from pathlib import Path

import numpy as np
import pandas as pd

from simulator import (
    generate_market_data,
    run_strategy,
)


def run_experiment(
    seeds=range(100),
    steps=2000,
    output_dir="outputs",
):

    output = Path(output_dir)

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    rows = []

    first_adaptive = None
    first_baseline = None

    for seed in seeds:

        market = generate_market_data(
            steps=steps,
            initial_price=100.0,
            seed=seed,
        )

        adaptive_results, adaptive = (
            run_strategy(
                market,
                "adaptive",
                execution_seed=seed + 10_000,
            )
        )

        baseline_results, baseline = (
            run_strategy(
                market,
                "baseline",
                execution_seed=seed + 20_000,
            )
        )

        if first_adaptive is None:

            first_adaptive = adaptive_results
            first_baseline = baseline_results

        rows.append(
            {
                "seed": seed,

                "adaptive_pnl":
                    adaptive["total_pnl"],

                "baseline_pnl":
                    baseline["total_pnl"],

                "adaptive_sharpe":
                    adaptive["sharpe_ratio"],

                "baseline_sharpe":
                    baseline["sharpe_ratio"],

                "adaptive_drawdown":
                    adaptive["maximum_drawdown"],

                "baseline_drawdown":
                    baseline["maximum_drawdown"],

                "adaptive_max_inventory":
                    adaptive["maximum_inventory"],

                "baseline_max_inventory":
                    baseline["maximum_inventory"],

                "adaptive_avg_inventory":
                    adaptive["average_abs_inventory"],

                "baseline_avg_inventory":
                    baseline["average_abs_inventory"],

                "adaptive_executions":
                    adaptive["executions"],

                "baseline_executions":
                    baseline["executions"],
            }
        )

    df = pd.DataFrame(rows)

    def ci95(series):

        x = np.asarray(
            series,
            dtype=float,
        )

        half_width = (
            1.96
            * x.std(ddof=1)
            / np.sqrt(len(x))
        )

        return (
            float(x.mean() - half_width),
            float(x.mean() + half_width),
        )

    adaptive_ci = ci95(
        df["adaptive_pnl"]
    )

    baseline_ci = ci95(
        df["baseline_pnl"]
    )

    summary = {

        "runs": len(df),

        "adaptive_mean_pnl":
            df["adaptive_pnl"].mean(),

        "baseline_mean_pnl":
            df["baseline_pnl"].mean(),

        "adaptive_median_pnl":
            df["adaptive_pnl"].median(),

        "baseline_median_pnl":
            df["baseline_pnl"].median(),

        "adaptive_pnl_std":
            df["adaptive_pnl"].std(
                ddof=1
            ),

        "baseline_pnl_std":
            df["baseline_pnl"].std(
                ddof=1
            ),

        "adaptive_mean_sharpe":
            df["adaptive_sharpe"].mean(),

        "baseline_mean_sharpe":
            df["baseline_sharpe"].mean(),

        "adaptive_mean_drawdown":
            df["adaptive_drawdown"].mean(),

        "baseline_mean_drawdown":
            df["baseline_drawdown"].mean(),

        "adaptive_mean_inventory":
            df["adaptive_avg_inventory"].mean(),

        "baseline_mean_inventory":
            df["baseline_avg_inventory"].mean(),

        "adaptive_win_rate":
            (
                df["adaptive_pnl"]
                > df["baseline_pnl"]
            ).mean(),

        "adaptive_pnl_ci95_low":
            adaptive_ci[0],

        "adaptive_pnl_ci95_high":
            adaptive_ci[1],

        "baseline_pnl_ci95_low":
            baseline_ci[0],

        "baseline_pnl_ci95_high":
            baseline_ci[1],
    }

    df.to_csv(
        output / "experiment_summary.csv",
        index=False,
    )

    pd.DataFrame(
        [summary]
    ).to_csv(
        output / "aggregate_results.csv",
        index=False,
    )

    first_adaptive.to_csv(
        output / "single_run_results.csv",
        index=False,
    )

    return (
        df,
        summary,
        first_adaptive,
        first_baseline,
    )


def make_plots(
    experiment_df,
    adaptive_results,
    baseline_results,
    output_dir="outputs",
):

    import matplotlib.pyplot as plt

    output = Path(output_dir)

    plt.figure(figsize=(12, 5))

    plt.plot(
        adaptive_results["market_price"],
        label="Observed Market Price",
    )

    plt.plot(
        adaptive_results["fair_value"],
        label="Estimated Fair Value",
    )

    plt.title(
        "Bayesian Fair-Value Estimation"
    )

    plt.xlabel("Simulation Step")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        output / "fair_value_estimation.png",
        dpi=150,
    )

    plt.close()

    plt.figure(figsize=(12, 5))

    plt.plot(
        adaptive_results["market_price"],
        label="Market Price",
    )

    plt.plot(
        adaptive_results["bid"],
        label="Adaptive Bid",
    )

    plt.plot(
        adaptive_results["ask"],
        label="Adaptive Ask",
    )

    plt.title(
        "Adaptive Bid / Ask Quotes"
    )

    plt.xlabel("Simulation Step")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        output / "adaptive_quotes.png",
        dpi=150,
    )

    plt.close()

    plt.figure(figsize=(12, 5))

    plt.plot(
        adaptive_results["portfolio_value"],
        label="Adaptive",
    )

    plt.plot(
        baseline_results["portfolio_value"],
        label="Fixed Spread",
    )

    plt.title(
        "Portfolio Value Comparison"
    )

    plt.xlabel("Simulation Step")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        output / "portfolio_comparison.png",
        dpi=150,
    )

    plt.close()

    plt.figure(figsize=(12, 5))

    plt.plot(
        adaptive_results["inventory"],
        label="Adaptive",
    )

    plt.plot(
        baseline_results["inventory"],
        label="Fixed Spread",
    )

    plt.title(
        "Inventory Exposure"
    )

    plt.xlabel("Simulation Step")
    plt.ylabel("Inventory")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        output / "inventory_exposure.png",
        dpi=150,
    )

    plt.close()

    plt.figure(figsize=(10, 5))

    plt.hist(
        experiment_df["adaptive_pnl"],
        bins=20,
        alpha=0.65,
        label="Adaptive P&L",
    )

    plt.hist(
        experiment_df["baseline_pnl"],
        bins=20,
        alpha=0.65,
        label="Baseline P&L",
    )

    plt.title(
        "P&L Distribution Across Independent Simulations"
    )

    plt.xlabel("Total P&L")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        output / "pnl_distribution.png",
        dpi=150,
    )

    plt.close()
