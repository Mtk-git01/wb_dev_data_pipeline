
import pandas as pd
from src.extract_aze_bulletin_common import add_country_fields
from src.config import AZE_CUSTOMER_ACCOUNTS_EBANKING_MONTHLY_SOURCE_NAME

def transform_aze_customer_accounts_ebanking_monthly(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    required = ['country_iso', 'month', 'bank_customers_total_people', 'customer_accounts_total_count']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if "period_date" in df.columns:
        df["period_date"] = pd.to_datetime(df["period_date"], errors="coerce")
    if "month" in df.columns:
        df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.to_period("M").dt.to_timestamp()
    numeric_cols = [c for c in df.columns if c not in ["country_name","country_iso","period_date","period_type","month","source_file","bulletin_period","source_name","load_timestamp"]]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    key_cols = ["country_iso"] + (["period_date","period_type"] if "period_date" in df.columns else ["month"])
    date_col = "period_date" if "period_date" in df.columns else "month"
    df = (
        df.dropna(subset=[date_col])
          .sort_values(key_cols)
          .drop_duplicates(subset=key_cols, keep="last")
          .reset_index(drop=True)
    )
    df["source_name"] = AZE_CUSTOMER_ACCOUNTS_EBANKING_MONTHLY_SOURCE_NAME
    df["load_timestamp"] = pd.Timestamp.utcnow()
    return df
