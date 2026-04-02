# Merton Model Credit Risk Engine

This project implements a **structural credit risk model (Merton model)** to estimate:

* Firm asset value and volatility
* Distance to default (DD)
* Default probability (PD)

The implementation is designed for **cross-sectional analysis across multiple firms**, with additional ranking and signal generation.

---

## Features

* Full **Merton model solver** using nonlinear root finding
* Estimation of:

  * Asset value
  * Asset volatility
  * Distance to default (DD)
  * Default probability (PD)
* Cross-sectional **ranking and signal generation**
* Clean data pipeline from raw inputs → model outputs
* Ready-to-run demo with sample dataset

---

## Project Structure

```text
project/
│
├── src/
│   ├── merton.py              # Core Merton model solver
│   ├── signals.py             # Ranking & signal generation
│   ├── data_utils.py          # Data loading & preprocessing
│   ├── run_demo.py            # End-to-end demo script
│
├── data/
│   ├── sample_inputs.csv      # Example dataset
│
├── requirements.txt
├── README.md
```

---

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the full pipeline:

```bash
python src/run_demo.py
```

This will:

1. Load sample data
2. Construct Merton model inputs
3. Solve for asset values and volatilities
4. Compute default probabilities
5. Generate cross-sectional signals
6. Print results

---

## Input Data Format

The input CSV must contain:

| Column         | Description             |
| -------------- | ----------------------- |
| ticker         | Company identifier      |
| date           | Observation date        |
| market_cap     | Equity market value     |
| equity_vol     | Equity volatility       |
| debt_short     | Short-term debt         |
| debt_long      | Long-term debt          |
| risk_free_rate | Risk-free interest rate |

---

## Methodology

### Merton Model

Equity is modeled as a **call option on firm assets**:

* Asset value and volatility are inferred by solving:

  * Equity value equation
  * Equity volatility relationship

The system is solved numerically using `scipy.optimize.root`.

---

### Key Outputs

* **Asset Value (V)**
* **Asset Volatility (σₐ)**
* **Distance to Default (DD)**
* **Default Probability (PD)**

Where:

* PD = Φ(−d₂)
* DD is computed in structural form using asset dynamics

---

### Signals

Cross-sectional signals are generated based on:

* Distance to default (higher = safer)
* Default probability (lower = safer)

Example:

* Top 20% strongest firms → **+1 signal**
* Bottom 20% weakest firms → **−1 signal**

---

## Example Output

The script prints a table including:

* Inputs (equity, debt, volatility)
* Model outputs (asset value, PD, DD)
* Rankings and signals

---

## Requirements

* Python 3.10+
* numpy
* scipy
* pandas

---

## Notes

* The model assumes **Black–Scholes dynamics for firm value**
* Default occurs if asset value falls below debt at maturity
* Results are **risk-neutral probabilities**, not real-world PDs
* Input quality (volatility, debt estimates) strongly affects outputs

---

## Purpose

This project demonstrates:

* Structural credit risk modeling
* Nonlinear system solving in finance
* Cross-sectional risk ranking
* Practical implementation of the Merton framework

---

## Author

This project is intended for **quantitative finance, risk modeling, and educational purposes**. Feel free to use and extend.
