from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "ticker",
    "date",
    "market_cap",
    "equity_vol",
    "debt_short",
    "debt_long",
    "risk_free_rate",
}


def load_input_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    numeric_cols = [
        "market_cap",
        "equity_vol",
        "debt_short",
        "debt_long",
        "risk_free_rate",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="raise")

    return df


def build_merton_dataset(
    df: pd.DataFrame,
    debt_weight_long: float = 0.5,
    horizon_years: float = 1.0,
) -> pd.DataFrame:
    out = df.copy()
    out["debt_face"] = out["debt_short"] + debt_weight_long * out["debt_long"]
    out["equity_value"] = out["market_cap"]
    out["horizon_years"] = horizon_years

    bad = (out["equity_value"] <= 0) | (out["equity_vol"] <= 0) | (out["debt_face"] <= 0)
    if bad.any():
        bad_names = out.loc[bad, "ticker"].tolist()
        raise ValueError(f"Non-positive inputs for: {bad_names}")

    return out


def annualized_vol_from_prices(prices: Iterable[float], periods_per_year: int = 252) -> float:
    s = pd.Series(list(prices), dtype=float).dropna()
    if len(s) < 3:
        raise ValueError("Need at least 3 prices to estimate volatility.")
    rets = np.log(s / s.shift(1)).dropna()
    return float(rets.std(ddof=1) * np.sqrt(periods_per_year))