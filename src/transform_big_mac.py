import pandas as pd
from datetime import datetime, timezone

from src.config import BIG_MAC_SOURCE_NAME


def transform_big_mac(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out["year"] = out["date"].dt.year.astype("Int64")

    out["country_name"] = out["name"]
    out["country_iso"] = out["iso_a3"]

    # 列名を分析向けに整理
    rename_map = {
        "local_price": "local_price",
        "dollar_price": "dollar_price",
        "USD_raw": "usd_raw_index",
        "USD_adjusted": "usd_adjusted_index",
        "GDP_dollar": "gdp_dollar",
    }

    for src, dst in rename_map.items():
        if src in out.columns:
            out[dst] = pd.to_numeric(out[src], errors="coerce")
        else:
            out[dst] = pd.NA

    out["source_name"] = BIG_MAC_SOURCE_NAME
    out["load_timestamp"] = datetime.now(timezone.utc)

    keep_cols = [
        "country_name",
        "country_iso",
        "date",
        "year",
        "currency_code",
        "local_price",
        "dollar_price",
        "usd_raw_index",
        "usd_adjusted_index",
        "gdp_dollar",
        "source_name",
        "load_timestamp",
    ]

    for col in keep_cols:
        if col not in out.columns:
            out[col] = pd.NA

    out = out[keep_cols].sort_values(["country_iso", "date"]).reset_index(drop=True)
    return out


def latest_non_null(df: pd.DataFrame) -> pd.DataFrame:
    work = df.dropna(subset=["dollar_price"]).copy()
    work = work.sort_values(["country_iso", "date"])
    latest = work.groupby("country_iso", as_index=False).tail(1).reset_index(drop=True)
    return latest