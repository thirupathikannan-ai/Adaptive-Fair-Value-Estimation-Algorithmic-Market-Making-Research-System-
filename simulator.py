import numpy as np
import pandas as pd

from fair_value import (
    BayesianFairValueEstimator,
    apply_order_flow_signal,
)

from market_maker import (
    AdaptiveMarketMaker,
    FixedSpreadMarketMaker,
)

from execution import ExecutionSimulator
from metrics import calculate_metrics


def generate_market_data(
    steps: int = 2000,
    initial_price: float = 100.0,
    seed: int = 42,
) -> pd.DataFrame:

    rng = np.random.default_rng(seed)

    latent_value = initial_price

    rows = []

    for t in range(steps):

        latent_value += rng.normal(
            0.0,
            0.04,
        )

        market_price = (
            latent_value
            + rng.normal(0.0, 0.30)
        )

        imbalance = np.clip(
            rng.normal(0.0, 0.30),
            -1.0,
            1.0,
        )

        rows.append(
            {
                "time": t,
                "market_price": market_price,
                "latent_value": latent_value,
                "imbalance": imbalance,
            }
        )

    return pd.DataFrame(rows)


class Portfolio:

    def __init__(
        self,
        initial_cash: float = 100_000.0,
    ):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.inventory = 0

    def execute(
        self,
        side: str,
        price: float,
        quantity: int,
    ):

        if side == "BUY":

            self.cash -= (
                price * quantity
            )

            self.inventory += quantity

        elif side == "SELL":

            self.cash += (
                price * quantity
            )

            self.inventory -= quantity

    def value(
        self,
        market_price: float,
    ):

        return (
            self.cash
            + self.inventory * market_price
        )


def run_strategy(
    data: pd.DataFrame,
    strategy_type: str,
    execution_seed: int,
    initial_cash: float = 100_000.0,
    max_inventory: int = 100,
):

    portfolio = Portfolio(
        initial_cash
    )

    execution = ExecutionSimulator(
        arrival_probability=0.20,
        seed=execution_seed,
    )

    if strategy_type == "adaptive":

        estimator = BayesianFairValueEstimator(
            mean=float(
                data.iloc[0]["market_price"]
            ),
            variance=4.0,
            observation_variance=1.0,
        )

        maker = AdaptiveMarketMaker()

    elif strategy_type == "baseline":

        maker = FixedSpreadMarketMaker()

    else:

        raise ValueError(
            "strategy_type must be "
            "'adaptive' or 'baseline'"
        )

    portfolio_values = []
    inventories = []
    fair_values = []
    bids = []
    asks = []

    executions = 0

    recent_returns = []

    for i, row in data.iterrows():

        market_price = float(
            row["market_price"]
        )

        imbalance = float(
            row["imbalance"]
        )

        if i > 0:

            previous = float(
                data.iloc[i - 1]["market_price"]
            )

            recent_returns.append(
                market_price / previous - 1.0
            )

        volatility = (
            float(
                np.std(
                    recent_returns[-20:]
                )
            )
            if len(recent_returns) >= 20
            else 0.003
        )

        if strategy_type == "adaptive":

            fair_value, posterior_variance = (
                estimator.update(
                    market_price
                )
            )

            fair_value = apply_order_flow_signal(
                fair_value,
                imbalance,
                sensitivity=0.05,
            )

            quote = maker.generate_quote(
                fair_value=fair_value,
                posterior_variance=posterior_variance,
                volatility=volatility,
                inventory=portfolio.inventory,
            )

        else:

            fair_value = market_price

            quote = maker.generate_quote(
                market_price
            )

        trade = execution.execute(
            bid=quote.bid,
            ask=quote.ask,
            market_price=market_price,
        )

        if trade is not None:

            projected = portfolio.inventory

            if trade.side == "BUY":
                projected += trade.quantity
            else:
                projected -= trade.quantity

            if abs(projected) <= max_inventory:

                portfolio.execute(
                    trade.side,
                    trade.price,
                    trade.quantity,
                )

                executions += 1

        portfolio_values.append(
            portfolio.value(
                market_price
            )
        )

        inventories.append(
            portfolio.inventory
        )

        fair_values.append(
            fair_value
        )

        bids.append(
            quote.bid
        )

        asks.append(
            quote.ask
        )

    results = data.copy()

    results["fair_value"] = fair_values
    results["bid"] = bids
    results["ask"] = asks
    results["portfolio_value"] = portfolio_values
    results["inventory"] = inventories

    metrics = calculate_metrics(
        portfolio_values,
        inventories,
        executions,
    )

    return results, metrics
