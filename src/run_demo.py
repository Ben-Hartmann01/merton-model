from __future__ import annotations

from pathlib import Path

import pandas as pd

from data_utils import build_merton_dataset, load_input_csv
from merton import MertonInputs, solve_merton
from signals import add_cross_sectional_signals


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    input_path = root / "data" / "sample_inputs.csv"

    df = load_input_csv(input_path)
    df = build_merton_dataset(df, debt_weight_long=0.5, horizon_years=1.0)

    results = []
    for row in df.itertuples(index=False):
        solved = solve_merton(
            MertonInputs(
                equity_value=float(row.equity_value),
                debt_face=float(row.debt_face),
                risk_free_rate=float(row.risk_free_rate),
                equity_vol=float(row.equity_vol),
                horizon_years=float(row.horizon_years),
            )
        )

        results.append(
            {
                "ticker": row.ticker,
                "date": row.date,
                "equity_value": row.equity_value,
                "debt_face": row.debt_face,
                "equity_vol": row.equity_vol,
                "asset_value": solved.asset_value,
                "asset_vol": solved.asset_vol,
                "distance_to_default": solved.distance_to_default,
                "default_probability": solved.default_probability,
            }
        )

    out = pd.DataFrame(results)
    out = add_cross_sectional_signals(out)

    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 20)
    print(out.round(6).to_string(index=False))


if __name__ == "__main__":
    main()