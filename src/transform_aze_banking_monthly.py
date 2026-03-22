import pandas as pd

from src.config import AZE_BANKING_MONTHLY_SOURCE_NAME


def transform_aze_banking_monthly(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Expected raw columns:
    - month
    - bank_total_assets_mn_azn
    - bank_loans_customers_mn_azn
    - bank_deposits_total_mn_azn
    """
    df = raw_df.copy()

    required = [
        "month",
        "bank_total_assets_mn_azn",
        "bank_loans_customers_mn_azn",
        "bank_deposits_total_mn_azn",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing Azerbaijan banking monthly columns: {missing}")

    df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.to_period("M").dt.to_timestamp()

    numeric_cols = [
        "bank_total_assets_mn_azn",
        "bank_loans_customers_mn_azn",
        "bank_deposits_total_mn_azn",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["month"]).copy()
    df = (
        df.sort_values("month")
        .drop_duplicates(subset=["month"], keep="last")
        .reset_index(drop=True)
    )

    df["source_name"] = AZE_BANKING_MONTHLY_SOURCE_NAME
    df["load_timestamp"] = pd.Timestamp.utcnow()

    return df