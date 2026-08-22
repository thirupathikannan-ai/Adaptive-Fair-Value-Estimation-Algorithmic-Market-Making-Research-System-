# Adaptive Fair-Value Estimation and Algorithmic Market-Making Research System

A quantitative research framework for studying **adaptive market making under uncertainty** using Bayesian fair-value estimation, order-flow information, volatility-aware spreads, inventory-aware pricing, stochastic execution, and risk-adjusted performance analysis.

---

## Overview

Market makers continuously provide bid and ask prices while managing uncertainty about the underlying fair value and their inventory exposure.

This project develops a research-oriented market-making simulator that dynamically adapts its quotes using:

- Bayesian fair-value estimation
- Posterior uncertainty
- Order-flow imbalance
- Short-term volatility
- Inventory exposure
- Adaptive bid-ask spreads
- Stochastic execution
- Portfolio accounting
- Risk-adjusted performance analysis

The adaptive strategy is evaluated against a **fixed-spread market-making baseline** using repeated independent simulations.

The objective is not to assume that adaptive market making is profitable. Instead, the system empirically studies the trade-off between:

```text
Fair-Value Estimation
        +
Order-Flow Information
        +
Spread Adaptation
        +
Inventory Control
        +
Stochastic Execution
        =
Market-Making Performance
```

---

# Research Question

> **Can an adaptive market maker using Bayesian fair-value estimation, order-flow information, volatility, and inventory risk produce better risk-controlled behavior than a fixed-spread market maker?**

The project evaluates this question experimentally rather than assuming the answer.

---

# Research Objectives

### Objective 1 — Estimate Fair Value

Construct a Bayesian estimator that updates the market maker's belief about latent fair value from noisy market observations.

### Objective 2 — Incorporate Market Microstructure Signals

Use order-flow imbalance as a bounded directional signal for short-term fair-value adjustment.

### Objective 3 — Control Inventory Risk

Modify the reservation price according to current inventory exposure.

### Objective 4 — Adapt Quoted Spreads

Widen or tighten the bid-ask spread according to market volatility and model uncertainty.

### Objective 5 — Evaluate Execution

Simulate stochastic order arrivals and execution while enforcing inventory limits.

### Objective 6 — Compare Strategies

Compare the adaptive strategy with a fixed-spread baseline over many independent simulation paths.

---

# System Architecture

```text
                         ┌─────────────────────┐
                         │   Synthetic Market  │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Market Price        │
                         │ Latent Value        │
                         │ Order Flow          │
                         │ Volatility          │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Bayesian Fair Value │
                         │ Estimator            │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Order-Flow           │
                         │ Adjustment           │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Inventory-Aware      │
                         │ Reservation Price    │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Volatility +         │
                         │ Uncertainty Spread   │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Adaptive Bid / Ask   │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Stochastic Execution │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Portfolio & Risk     │
                         │ Accounting            │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Multi-Seed Research  │
                         │ Evaluation            │
                         └──────────────────────┘
```

---

# Mathematical Model

## 1. Bayesian Fair-Value Estimation

The market price is treated as a noisy observation of an underlying latent fair value.

Let:

```text
Prior mean       = μ
Prior variance   = σ²
Observation      = y
Observation var. = τ²
```

The Gaussian conjugate posterior is:

```text
Posterior Variance =
1 / (1/σ² + 1/τ²)
```

and:

```text
Posterior Mean =
Posterior Variance ×
(μ/σ² + y/τ²)
```

The posterior mean represents the updated fair-value estimate.

The posterior variance represents estimation uncertainty.

---

# 2. Order-Flow Imbalance

The simulator generates normalized order-flow imbalance:

```text
Imbalance =
(Bid Quantity - Ask Quantity)
/
(Bid Quantity + Ask Quantity)
```

The signal is bounded to:

```text
[-1, +1]
```

The fair-value estimate is then adjusted using a controlled sensitivity parameter:

```text
Adjusted Fair Value =
Bayesian Fair Value
+
Sensitivity × Order-Flow Imbalance
```

This prevents the microstructure signal from completely dominating the Bayesian estimate.

---

# 3. Inventory-Aware Reservation Price

Inventory creates asymmetric risk.

The reservation price is defined as:

```text
Reservation Price =
Fair Value
-
Inventory Penalty × Inventory
```

Therefore:

```text
Positive Inventory
        ↓
Lower Reservation Price
        ↓
Greater incentive to sell
```

and:

```text
Negative Inventory
        ↓
Higher Reservation Price
        ↓
Greater incentive to buy
```

This creates a basic inventory-control mechanism.

---

# 4. Adaptive Spread

The adaptive spread incorporates both volatility and estimation uncertainty:

```text
Spread =
Base Spread
+
Volatility Multiplier × Volatility
+
Uncertainty Multiplier × Posterior Standard Deviation
```

The quotes are:

```text
Bid =
Reservation Price - Spread / 2

Ask =
Reservation Price + Spread / 2
```

Therefore, the market maker can quote wider markets when uncertainty or volatility increases.

---

# 5. Fixed-Spread Baseline

A fixed-spread market maker provides the control strategy:

```text
Bid =
Market Price - Fixed Spread / 2

Ask =
Market Price + Fixed Spread / 2
```

Both strategies operate under the same synthetic market framework.

---

# 6. Stochastic Execution

Execution is modeled probabilistically.

At each simulation step:

```text
No Execution
      OR
Buy Execution
      OR
Sell Execution
```

The strategy also enforces a maximum inventory limit.

This prevents unrealistic unlimited inventory accumulation.

---

# 7. Portfolio Accounting

The portfolio tracks:

```text
Cash
Inventory
Market Value
Portfolio Value
```

Portfolio value is:

```text
Portfolio Value =
Cash + Inventory × Market Price
```

This provides the basis for P&L and risk calculations.

---

# Performance Metrics

The system measures:

- Total P&L
- Median P&L
- P&L standard deviation
- Sharpe ratio
- Maximum drawdown
- Maximum inventory
- Average absolute inventory
- Number of executions
- Adaptive win rate
- 95% confidence interval for P&L

This allows the strategy to be evaluated on both **return and risk**.

---

# Experimental Design

A single simulation can be misleading because stochastic market-making performance depends on the generated market path and execution path.

Therefore, the project performs:

```text
100 Independent Simulations
```

For every seed:

```text
                 Same Market Path
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
      Adaptive Strategy    Fixed-Spread
             │                   │
             ▼                   ▼
       Risk Metrics         Risk Metrics
             │                   │
             └─────────┬─────────┘
                       ▼
                Statistical
                 Comparison
```

The aggregate experiment calculates:

- Mean P&L
- Median P&L
- P&L standard deviation
- Mean Sharpe ratio
- Mean drawdown
- Mean inventory
- Adaptive win rate
- 95% P&L confidence intervals

---

# Actual Research Result

The current implementation was evaluated across **100 independent simulations**.

| Metric | Adaptive | Fixed Spread |
|---|---:|---:|
| Mean P&L | -46.45 | 12.18 |
| Median P&L | -36.11 | 21.13 |
| Mean Sharpe | -0.0434 | 0.0070 |
| Mean Drawdown | 0.1564% | 0.3112% |
| Mean Inventory | 30.07 | 87.50 |
| Win Rate | 50.00% | — |

### 95% P&L Confidence Interval

| Strategy | 95% CI |
|---|---:|
| Adaptive | [-59.84, -33.05] |
| Fixed Spread | [-20.70, 45.06] |

---

# Results Interpretation

The experiment does **not** demonstrate that the adaptive strategy dominates the fixed-spread baseline in raw P&L.

Instead, the adaptive strategy exhibits substantially lower average inventory exposure and lower average drawdown.

```text
                       Adaptive      Baseline

Mean Inventory           30.08         87.50

Mean Drawdown            0.1564%       0.3112%

Mean P&L                 -46.45        12.18
```

This demonstrates an important market-making trade-off:

```text
Lower Inventory Risk
        ≠
Automatically Higher P&L
```

The experiment therefore highlights that market-making performance depends on the interaction between:

```text
Spread Capture
+
Execution Probability
+
Fair-Value Accuracy
+
Adverse Selection
+
Inventory Risk
+
Market Dynamics
```

The negative adaptive P&L under this particular synthetic model is treated as a research finding rather than being hidden or artificially optimized away.

---

# Visualizations

The experiment generates five visualizations.

### 1. Bayesian Fair-Value Estimation

```text
outputs/fair_value_estimation.png
```

Compares observed market price against the estimated fair value.

### 2. Adaptive Quotes

```text
outputs/adaptive_quotes.png
```

Shows the adaptive bid and ask around the estimated fair value.

### 3. Portfolio Comparison

```text
outputs/portfolio_comparison.png
```

Compares portfolio value for adaptive and fixed-spread strategies.

### 4. Inventory Exposure

```text
outputs/inventory_exposure.png
```

Compares inventory behavior between the two strategies.

### 5. P&L Distribution

```text
outputs/pnl_distribution.png
```

Shows the distribution of P&L across the independent simulation runs.

---

# Reproducibility

The project uses explicit random seeds.

A single simulation can be reproduced using:

```python
seed = 42
```

The multi-run experiment uses:

```python
range(100)
```

to evaluate the strategy across 100 different random market paths.

This makes the experiment reproducible while avoiding dependence on a single stochastic outcome.

---

# Project Structure

```text
Adaptive-Fair-Value-Estimation-Algorithmic-Market-Making/
│
├── README.md
│
├── main.py
│
├── fair_value.py
│
├── market_maker.py
│
├── execution.py
│
├── simulator.py
│
├── metrics.py
│
├── experiment.py
│
├── requirements.txt
│
├── .gitignore
│
└── outputs/
    ├── aggregate_results.csv
    ├── experiment_summary.csv
    ├── single_run_results.csv
    ├── fair_value_estimation.png
    ├── adaptive_quotes.png
    ├── portfolio_comparison.png
    ├── inventory_exposure.png
    └── pnl_distribution.png
```

---

# Installation

Clone the repository:

```bash
git clone
https://github.com/thirupathikannan-ai/Adaptive-Fair-Value-Estimation-Algorithmic-Market-Making-Research-System-.git
```

Enter the project directory:

```bash
cd Adaptive-Fair-Value-Estimation-Algorithmic-Market-Making
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run the Complete Research Experiment

Run:

```bash
python main.py
```

The program automatically creates:

```text
outputs/
```

with:

```text
aggregate_results.csv
experiment_summary.csv
single_run_results.csv
fair_value_estimation.png
adaptive_quotes.png
portfolio_comparison.png
inventory_exposure.png
pnl_distribution.png
```

---

# Example Terminal Output

```text
============================================================
ADAPTIVE FAIR-VALUE & MARKET-MAKING RESEARCH SYSTEM
============================================================

Runs                    : 100

Adaptive mean P&L       : -46.45
Baseline mean P&L       : 12.18

Adaptive median P&L     : -36.11
Baseline median P&L     : 21.13

Adaptive mean Sharpe    : -0.0434
Baseline mean Sharpe    : 0.0070

Adaptive mean drawdown  : 0.1564%
Baseline mean drawdown  : 0.3112%

Adaptive mean inventory : 30.08
Baseline mean inventory : 87.50

Adaptive win rate       : 50.00%

Adaptive 95% P&L CI     : [-59.84, -33.05]
Baseline 95% P&L CI     : [-20.70, 45.06]

============================================================
```

---

# Limitations

The current simulator uses a simplified synthetic market.

It does not yet model:

- Full Level-2 order-book dynamics
- Price-time priority
- Queue position
- Partial fills
- Order cancellation
- Latency
- Market impact
- Exchange fees
- Maker/taker rebates
- Transaction costs
- Slippage
- Adverse-selection estimation
- Real historical order-book data
- Production trading infrastructure

Therefore:

> **The simulated results should not be interpreted as evidence of live-trading profitability.**

---

# Future Research

## 1. Limit Order Book Integration

Integrate the strategy with historical Level-2 order-book data.

## 2. Queue Position Modeling

Estimate execution probability based on queue position.

## 3. Partial Fills

Replace binary fills with realistic partial execution.

## 4. Latency Modeling

Introduce:

```text
Market Observation
        ↓
Signal Generation
        ↓
Order Submission
        ↓
Exchange Latency
        ↓
Execution
```

## 5. Transaction Costs

Model:

```text
Exchange Fees
+
Maker/Taker Rebates
+
Slippage
+
Market Impact
```

## 6. Advanced Bayesian Models

Potential extensions:

```text
Kalman Filter
Hidden Markov Model
Regime-Switching Model
Particle Filter
```

## 7. Parameter Sensitivity Analysis

Evaluate sensitivity to:

```text
Inventory Penalty
Base Spread
Volatility Multiplier
Uncertainty Multiplier
Execution Probability
Order-Flow Sensitivity
```

## 8. Out-of-Sample Evaluation

Separate:

```text
Calibration
     ↓
Validation
     ↓
Out-of-Sample Testing
```

to reduce parameter overfitting.

---

# Technologies

```text
Python
NumPy
Pandas
Matplotlib
Probability
Bayesian Statistics
Monte Carlo Simulation
Statistical Analysis
Market Microstructure
Algorithmic Trading
Risk Management
Quantitative Research
```

---

# Quantitative Concepts Demonstrated

```text
Bayesian Inference
Gaussian Conjugate Updating
Expected Value
Probability
Statistical Estimation
Uncertainty Quantification
Order-Flow Imbalance
Market Microstructure
Bid-Ask Spreads
Inventory Risk
Stochastic Execution
Monte Carlo Simulation
Sharpe Ratio
Maximum Drawdown
Confidence Intervals
Baseline Comparison
Parameter Sensitivity
```

---

# Resume Description

### Adaptive Fair-Value Estimation & Algorithmic Market-Making Research System

**Python | Bayesian Statistics | Probability | Market Microstructure**

```text
• Built a Bayesian fair-value estimator with posterior uncertainty and order-flow adjustments for adaptive market making.

• Developed inventory-aware reservation pricing and volatility/uncertainty-dependent bid-ask spreads with stochastic execution.

• Implemented portfolio accounting and risk analytics covering P&L, Sharpe ratio, maximum drawdown, inventory exposure, and execution statistics.

• Evaluated adaptive versus fixed-spread market making across 100 independent simulations using aggregate statistics and 95% confidence intervals.
```

---

# Why This Project Is Relevant to Quantitative Trading

This project demonstrates several skills relevant to quantitative trading research:

```text
Probabilistic Modeling
        +
Statistical Inference
        +
Market Microstructure
        +
Algorithm Design
        +
Simulation
        +
Risk Management
        +
Experimental Evaluation
```

The project emphasizes **hypothesis → model → simulation → baseline → statistical evaluation → interpretation**, rather than simply producing a trading bot.

---

# Disclaimer

This project is intended for educational and quantitative research purposes only.

It does not constitute financial advice, investment advice, or a live trading strategy.

The reported results depend on the assumptions and parameters of the synthetic market and execution model.

---

# Author

**Thirupathi Kannan K**

GitHub:

https://github.com/thirupathikannan-ai

---

# License

This project is provided for educational and quantitative research purposes.
