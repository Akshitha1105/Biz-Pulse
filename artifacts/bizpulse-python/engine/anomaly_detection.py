"""
BizPulse Anomaly Detection Engine
Time-series analysis on GST filing trends, turnover patterns, and compliance rates.
Simulates: Kafka streaming + statistical anomaly detection pipeline
"""

import numpy as np
import pandas as pd
from typing import Optional


def generate_district_gst_timeseries(
    district: str, months: int = 12, seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Generate synthetic monthly GST filing timeseries for a district.
    Injects anomalies for Dharwad and Belagavi to match the demo alerts.
    """
    rng = np.random.default_rng(seed or hash(district) % 10000)

    # Base filing counts with seasonal pattern
    base = rng.integers(800, 2400)
    seasonal = np.sin(np.linspace(0, 2 * np.pi, months)) * base * 0.12
    noise = rng.normal(0, base * 0.04, months)
    values = base + seasonal + noise
    values = np.clip(values, base * 0.4, base * 2.0)

    # Inject anomaly: last 2 months show a drop for Dharwad
    if district in ("Dharwad", "Hubli-Dharwad"):
        drop_factor = 0.77  # 23% drop
        values[-2:] = values[-2:] * drop_factor

    # Inject anomaly: cluster spike for Belagavi
    if district == "Belagavi":
        values[-1] = values[-1] * 0.60  # 40% drop last month

    dates = pd.date_range(end="2025-05-01", periods=months, freq="MS")
    return pd.DataFrame({"month": dates, "filings": values.astype(int), "district": district})


def detect_anomalies_zscore(series: pd.Series, threshold: float = 2.0) -> list[int]:
    """Return indices where the value is an anomaly (|z-score| > threshold)."""
    mean = series.mean()
    std = series.std()
    if std == 0:
        return []
    z_scores = np.abs((series - mean) / std)
    return list(np.where(z_scores > threshold)[0])


def compute_trend(values: list[float]) -> str:
    """Simple linear trend direction."""
    if len(values) < 2:
        return "stable"
    slope = np.polyfit(range(len(values)), values, 1)[0]
    if slope > 0.5:
        return "increasing"
    elif slope < -0.5:
        return "decreasing"
    return "stable"


def generate_compliance_rate_timeseries(
    sector: str, months: int = 12
) -> pd.DataFrame:
    """Generate synthetic compliance rate trend for a sector."""
    rng = np.random.default_rng(hash(sector) % 9999)
    base_rate = rng.uniform(65, 98)
    trend = rng.uniform(-0.3, 0.5)
    noise = rng.normal(0, 1.2, months)
    rates = base_rate + np.arange(months) * trend + noise
    rates = np.clip(rates, 40, 100)
    dates = pd.date_range(end="2025-05-01", periods=months, freq="MS")
    return pd.DataFrame({"month": dates, "compliance_rate": rates, "sector": sector})


def generate_turnover_forecast(
    historical: list[float], periods_ahead: int = 3
) -> list[float]:
    """
    Simple linear extrapolation of turnover for forecast.
    In production: replace with ARIMA / Prophet.
    """
    x = np.arange(len(historical))
    coeffs = np.polyfit(x, historical, 1)
    future_x = np.arange(len(historical), len(historical) + periods_ahead)
    forecast = np.polyval(coeffs, future_x)
    return [max(0, round(float(v), 1)) for v in forecast]


def compute_anomaly_summary(df: pd.DataFrame) -> dict:
    """Summarize anomalies detected in a timeseries DataFrame."""
    anomaly_indices = detect_anomalies_zscore(df["filings"])
    trend = compute_trend(df["filings"].tolist())
    pct_change = 0.0
    if len(df) >= 2:
        last = df["filings"].iloc[-1]
        prev_avg = df["filings"].iloc[-3:-1].mean()
        if prev_avg > 0:
            pct_change = round((last - prev_avg) / prev_avg * 100, 1)
    return {
        "anomaly_count": len(anomaly_indices),
        "anomaly_indices": anomaly_indices,
        "trend": trend,
        "pct_change_recent": pct_change,
        "latest_value": int(df["filings"].iloc[-1]),
        "average_value": int(df["filings"].mean()),
    }
