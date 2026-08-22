from dataclasses import dataclass

import numpy as np


@dataclass
class Trade:
    side: str
    price: float
    quantity: int


class ExecutionSimulator:
    """Simplified stochastic execution model."""

    def __init__(
        self,
        arrival_probability: float = 0.20,
        seed: int = 42,
    ):
        self.arrival_probability = arrival_probability
        self.rng = np.random.default_rng(seed)

    def execute(
        self,
        bid: float,
        ask: float,
        market_price: float,
    ) -> Trade | None:

        if self.rng.random() > self.arrival_probability:
            return None

        bid_distance = abs(
            market_price - bid
        )

        ask_distance = abs(
            ask - market_price
        )

        if bid_distance <= ask_distance:
            return Trade(
                side="BUY",
                price=bid,
                quantity=1,
            )

        return Trade(
            side="SELL",
            price=ask,
            quantity=1,
        )
