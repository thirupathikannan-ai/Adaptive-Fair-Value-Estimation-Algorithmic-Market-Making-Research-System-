from pathlib import Path

from experiment import (
    run_experiment,
    make_plots,
)


def main():

    output_dir = Path("outputs")

    (
        df,
        summary,
        adaptive,
        baseline,
    ) = run_experiment(
        seeds=range(100),
        steps=2000,
        output_dir=output_dir,
    )

    make_plots(
        df,
        adaptive,
        baseline,
        output_dir=output_dir,
    )

    print("=" * 60)

    print(
        "ADAPTIVE FAIR-VALUE & "
        "MARKET-MAKING RESEARCH SYSTEM"
    )

    print("=" * 60)

    print(
        f"Runs                    : "
        f"{summary['runs']}"
    )

    print()

    print(
        f"Adaptive mean P&L       : "
        f"{summary['adaptive_mean_pnl']:.2f}"
    )

    print(
        f"Baseline mean P&L       : "
        f"{summary['baseline_mean_pnl']:.2f}"
    )

    print(
        f"Adaptive median P&L     : "
        f"{summary['adaptive_median_pnl']:.2f}"
    )

    print(
        f"Baseline median P&L     : "
        f"{summary['baseline_median_pnl']:.2f}"
    )

    print()

    print(
        f"Adaptive mean Sharpe    : "
        f"{summary['adaptive_mean_sharpe']:.4f}"
    )

    print(
        f"Baseline mean Sharpe    : "
        f"{summary['baseline_mean_sharpe']:.4f}"
    )

    print()

    print(
        f"Adaptive mean drawdown  : "
        f"{summary['adaptive_mean_drawdown']:.4%}"
    )

    print(
        f"Baseline mean drawdown  : "
        f"{summary['baseline_mean_drawdown']:.4%}"
    )

    print()

    print(
        f"Adaptive mean inventory : "
        f"{summary['adaptive_mean_inventory']:.2f}"
    )

    print(
        f"Baseline mean inventory : "
        f"{summary['baseline_mean_inventory']:.2f}"
    )

    print()

    print(
        f"Adaptive win rate       : "
        f"{summary['adaptive_win_rate']:.2%}"
    )

    print()

    print(
        "Adaptive 95% P&L CI    : "
        f"[{summary['adaptive_pnl_ci95_low']:.2f}, "
        f"{summary['adaptive_pnl_ci95_high']:.2f}]"
    )

    print(
        "Baseline 95% P&L CI    : "
        f"[{summary['baseline_pnl_ci95_low']:.2f}, "
        f"{summary['baseline_pnl_ci95_high']:.2f}]"
    )

    print("=" * 60)

    print(
        f"Outputs written to: "
        f"{output_dir.resolve()}"
    )


if __name__ == "__main__":
    main()
