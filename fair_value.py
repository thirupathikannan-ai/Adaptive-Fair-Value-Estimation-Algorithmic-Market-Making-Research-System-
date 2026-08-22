from dataclasses import dataclass


@dataclass
class BayesianFairValueEstimator:
    """Gaussian conjugate Bayesian fair-value estimator."""

    mean: float
    variance: float
    observation_variance: float

    def update(self, observation: float) -> tuple[float, float]:
        prior_precision = 1.0 / self.variance
        observation_precision = 1.0 / self.observation_variance

        posterior_variance = 1.0 / (
            prior_precision + observation_precision
        )

        posterior_mean = posterior_variance * (
            prior_precision * self.mean
            + observation_precision * observation
        )

        self.mean = posterior_mean
        self.variance = posterior_variance

        return self.mean, self.variance


def apply_order_flow_signal(
    fair_value: float,
    imbalance: float,
    sensitivity: float = 0.05,
) -> float:
    """Apply a bounded order-flow adjustment."""

    imbalance = max(-1.0, min(1.0, imbalance))

    return fair_value + sensitivity * imbalance
