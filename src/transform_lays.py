import pandas as pd
from datetime import datetime, timezone

from src.config import (
    LAYS_INDICATOR_CODE,
    LAYS_INDICATOR_NAME,
    LAYS_SOURCE_NAME,
)


def transform_wb_indicator(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["country_name"] = out["country"].apply(
        lambda x: x["value"] if isinstance(x, dict) else None
    )
    out["country_iso"] = out["countryiso3code"]
    out["indicator_name"] = out["indicator"].apply(
        lambda x: x["value"] if isinstance(x, dict) else None
    )
    out["year"] = pd.to_numeric(out["date"], errors="coerce").astype("Int64")
    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    out["decimal_places"] = pd.to_numeric(out["decimal"], errors="coerce").astype("Int64")

    out["indicator_code"] = LAYS_INDICATOR_CODE
    out["indicator_name"] = out["indicator_name"].fillna(LAYS_INDICATOR_NAME)
    out["source_name"] = LAYS_SOURCE_NAME
    out["load_timestamp"] = datetime.now(timezone.utc)

    keep_cols = [
        "country_name",
        "country_iso",
        "year",
        "value",
        "indicator_code",
        "indicator_name",
        "obs_status",
        "decimal_places",
        "source_name",
        "load_timestamp",
    ]

    for col in keep_cols:
        if col not in out.columns:
            out[col] = pd.NA

    out = out[keep_cols].sort_values(["country_iso", "year"]).reset_index(drop=True)
    return out


def latest_non_null(df: pd.DataFrame) -> pd.DataFrame:
    work = df.dropna(subset=["value"]).copy()
    work = work.sort_values(["country_iso", "year"])
    latest = work.groupby("country_iso", as_index=False).tail(1).reset_index(drop=True)
    return latest