import pandas as pd

from src.config import AZE_MACRO_MONTHLY_SOURCE_NAME


def build_aze_macro_monthly(
    cpi_df: pd.DataFrame,
    reserves_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine official CPI and official FX reserves into a monthly macro table.
    """
    cpi = cpi_df.copy()
    reserves = reserves_df.copy()

    cpi["month"] = pd.to_datetime(cpi["month"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    reserves["month"] = pd.to_datetime(reserves["month"], errors="coerce").dt.to_period("M").dt.to_timestamp()

    if "source_url" in cpi.columns:
        cpi = cpi.drop(columns=["source_url"])
    if "source_url" in reserves.columns:
        reserves = reserves.drop(columns=["source_url"])

    df = pd.merge(cpi, reserves, on="month", how="outer")

    df["cpi_yoy"] = pd.to_numeric(df["cpi_yoy"], errors="coerce")
    df["official_fx_reserves_usd_mn"] = pd.to_numeric(df["official_fx_reserves_usd_mn"], errors="coerce")

    df = (
        df.sort_values("month")
          .drop_duplicates(subset=["month"], keep="last")
          .reset_index(drop=True)
    )

    df["source_name"] = AZE_MACRO_MONTHLY_SOURCE_NAME
    df["load_timestamp"] = pd.Timestamp.utcnow()
    return df