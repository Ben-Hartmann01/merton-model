from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, sqrt

import numpy as np
from scipy.optimize import root
from scipy.stats import norm


@dataclass
class MertonInputs:
    equity_value: float
    debt_face: float
    risk_free_rate: float
    equity_vol: float
    horizon_years: float = 1.0


@dataclass
class MertonResult:
    asset_value: float
    asset_vol: float
    distance_to_default: float
    default_probability: float
    d1: float
    d2: float


def _validate_inputs(x: MertonInputs) -> None:
    if x.equity_value <= 0:
        raise ValueError("equity_value must be > 0")
    if x.debt_face <= 0:
        raise ValueError("debt_face must be > 0")
    if x.equity_vol <= 0:
        raise ValueError("equity_vol must be > 0")
    if x.horizon_years <= 0:
        raise ValueError("horizon_years must be > 0")


def _d1_d2(asset_value: float, debt_face: float, r: float, asset_vol: float, t: float) -> tuple[float, float]:
    vol_sqrt_t = asset_vol * sqrt(t)
    d1 = (log(asset_value / debt_face) + (r + 0.5 * asset_vol**2) * t) / vol_sqrt_t
    d2 = d1 - vol_sqrt_t
    return d1, d2


def _equations(
    vars_: np.ndarray,
    equity_value: float,
    debt_face: float,
    r: float,
    equity_vol: float,
    t: float,
) -> np.ndarray:
    asset_value, asset_vol = vars_

    if asset_value <= 0 or asset_vol <= 0:
        return np.array([1e9, 1e9], dtype=float)

    d1, d2 = _d1_d2(asset_value, debt_face, r, asset_vol, t)

    equity_model = asset_value * norm.cdf(d1) - debt_face * exp(-r * t) * norm.cdf(d2)
    sigma_equity_model = (asset_value / equity_value) * norm.cdf(d1) * asset_vol

    return np.array(
        [
            equity_model - equity_value,
            sigma_equity_model - equity_vol,
        ],
        dtype=float,
    )


def solve_merton(inputs: MertonInputs) -> MertonResult:
    _validate_inputs(inputs)

    e = inputs.equity_value
    d = inputs.debt_face
    r = inputs.risk_free_rate
    sigma_e = inputs.equity_vol
    t = inputs.horizon_years

    x0 = np.array(
        [
            e + d * exp(-r * t),
            sigma_e * e / (e + d),
        ],
        dtype=float,
    )
    x0[1] = max(x0[1], 1e-4)

    sol = root(
        _equations,
        x0=x0,
        args=(e, d, r, sigma_e, t),
        method="hybr",
    )

    if not sol.success:
        raise RuntimeError(f"Merton solve failed: {sol.message}")

    asset_value = float(sol.x[0])
    asset_vol = float(sol.x[1])

    if asset_value <= 0 or asset_vol <= 0:
        raise RuntimeError("Solved asset value or asset volatility is non-positive.")

    d1, d2 = _d1_d2(asset_value, d, r, asset_vol, t)

    # Risk-neutral default probability over horizon T
    pd = float(norm.cdf(-d2))

    # Distance to default in the common structural-model style
    dd = float((log(asset_value / d) + (r - 0.5 * asset_vol**2) * t) / (asset_vol * sqrt(t)))

    return MertonResult(
        asset_value=asset_value,
        asset_vol=asset_vol,
        distance_to_default=dd,
        default_probability=pd,
        d1=float(d1),
        d2=float(d2),
    )