from __future__ import annotations

import pandas as pd


def add_cross_sectional_signals(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "distance_to_default" not in out.columns or "default_probability" not in out.columns:
        raise ValueError("Expected distance_to_default and default_probability columns.")

    out["dd_rank_desc"] = out["distance_to_default"].rank(ascending=False, method="dense")
    out["pd_rank_asc"] = out["default_probability"].rank(ascending=True, method="dense")

    n = len(out)
    if n == 0:
        return out

    out["dd_percentile"] = out["distance_to_default"].rank(pct=True)
    out["pd_percentile"] = out["default_probability"].rank(pct=True, ascending=False)

    # Simple example signals:
    # +1 strongest balance sheets, -1 weakest balance sheets
    out["signal_dd"] = 0
    out.loc[out["dd_percentile"] >= 0.8, "signal_dd"] = 1
    out.loc[out["dd_percentile"] <= 0.2, "signal_dd"] = -1

    out["signal_pd"] = 0
    out.loc[out["default_probability"].rank(pct=True, ascending=False) >= 0.8, "signal_pd"] = -1
    out.loc[out["default_probability"].rank(pct=True, ascending=False) <= 0.2, "signal_pd"] = 1

    return out.sort_values("distance_to_default", ascending=False).reset_index(drop=True)