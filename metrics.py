import numpy as np


def calculate_metrics(
    portfolio_values,
    inventories,
    executions,
):
    values = np.asarray(
        portfolio_values,
        dtype=float,
    )

    inventory = np.asarray(
        inventories,
        dtype=float,
    )

    changes = np.diff(values)

    total_pnl = float(
        values[-1] - values[0]
    )

    if (
        len(changes) > 1
        and np.std(changes, ddof=1) > 0
    ):
        sharpe = (
            np.mean(changes)
            / np.std(changes, ddof=1)
        ) * np.sqrt(len(changes))
    else:
        sharpe = 0.0

    running_peak = np.maximum.accumulate(
        values
    )

    drawdown = (
        values - running_peak
    ) / running_peak

    maximum_drawdown = float(
        abs(np.min(drawdown))
    )

    return {
        "initial_value": float(values[0]),
        "final_value": float(values[-1]),
        "total_pnl": total_pnl,
        "sharpe_ratio": float(sharpe),
        "maximum_drawdown": maximum_drawdown,
        "maximum_inventory": int(
            np.max(np.abs(inventory))
        ),
        "average_abs_inventory": float(
            np.mean(np.abs(inventory))
        ),
        "executions": int(executions),
    }
