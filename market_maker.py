from dataclasses import dataclass


@dataclass
class Quote:
    bid: float
    ask: float
    reservation_price: float
    spread: float


class AdaptiveMarketMaker:
    """Inventory- and uncertainty-aware market maker."""

    def __init__(
        self,
        base_spread: float = 0.08,
        volatility_multiplier: float = 25.0,
        uncertainty_multiplier: float = 0.02,
        inventory_penalty: float = 0.015,
    ):
        self.base_spread = base_spread
        self.volatility_multiplier = volatility_multiplier
        self.uncertainty_multiplier = uncertainty_multiplier
        self.inventory_penalty = inventory_penalty

    def generate_quote(
        self,
        fair_value: float,
        posterior_variance: float,
        volatility: float,
        inventory: int,
    ) -> Quote:

        reservation_price = (
            fair_value
            - self.inventory_penalty * inventory
        )

        posterior_std = posterior_variance ** 0.5

        spread = (
            self.base_spread
            + self.volatility_multiplier * volatility
            + self.uncertainty_multiplier * posterior_std
        )

        spread = max(
            spread,
            self.base_spread,
        )

        return Quote(
            bid=reservation_price - spread / 2.0,
            ask=reservation_price + spread / 2.0,
            reservation_price=reservation_price,
            spread=spread,
        )


class FixedSpreadMarketMaker:
    """Simple fixed-spread baseline."""

    def __init__(self, spread: float = 0.08):
        self.spread = spread

    def generate_quote(
        self,
        market_price: float,
    ) -> Quote:

        return Quote(
            bid=market_price - self.spread / 2.0,
            ask=market_price + self.spread / 2.0,
            reservation_price=market_price,
            spread=self.spread,
        )
