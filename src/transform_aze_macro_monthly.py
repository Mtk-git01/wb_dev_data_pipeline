import pandas as pd

from src.config import AZE_MACRO_MONTHLY_SOURCE_NAME


def transform_aze_macro_monthly(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Expected raw columns:
    - month
    - cpi_yoy
    - official_fx_reserves_usd_mn
    """
    df = raw_df.copy()

    required = ["month", "cpi_yoy", "official_fx_reserves_usd_mn"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing Azerbaijan macro monthly columns: {missing}")

    df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    df["cpi_yoy"] = pd.to_numeric(df["cpi_yoy"], errors="coerce")
    df["official_fx_reserves_usd_mn"] = pd.to_numeric(df["official_fx_reserves_usd_mn"], errors="coerce")

    df = df.dropna(subset=["month"]).copy()
    df = (
        df.sort_values("month")
        .drop_duplicates(subset=["month"], keep="last")
        .reset_index(drop=True)
    )

    df["source_name"] = AZE_MACRO_MONTHLY_SOURCE_NAME
    df["load_timestamp"] = pd.Timestamp.utcnow()

    return df