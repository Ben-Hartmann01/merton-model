# Merton Model Signals

This project implements a structural credit-risk model based on the Merton framework and converts the outputs into simple cross-sectional asset signals. 

# Inputs
- equity value (market cap)
- equity volatility
- debt proxy (st_debt + 0.5 * lt_debt; this is standard)
- risk-free rate
- horizon

# Method
Equity is modeled as a call option on firm assets. The code solves jointly for:
- asset value
- asset vola

# It then computes:
- distance to default
- default prob
- simple ranking-based signals

## Data
The original research version used Bloomberg inputs.  
This public version uses reproducible CSV inputs and can be extended with public market and filing data. Its a demonstration of the methodology.


## Run
```bash
python src/run_demo.py