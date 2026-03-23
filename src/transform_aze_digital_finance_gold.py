import pandas as pd
from src.config import AZE_DIGITAL_FINANCE_SOURCE_NAME
from src.extract_aze_bulletin_common import safe_merge_periodic


def _normalize_period_type(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip().str.lower()

    mapping = {
        "monthly": "month",
        "month": "month",
        "m": "month",
        "quarterly": "quarter",
        "quarter": "quarter",
        "q": "quarter",
        "yearly": "year",
        "annual": "year",
        "year": "year",
        "y": "year",
    }
    return s.map(mapping).fillna(s)


def _to_periodic_month(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["period_date"] = pd.to_datetime(out["month"], errors="coerce")
    out["period_type"] = "month"

    keep_cols = [
        c for c in out.columns
        if c not in ["month", "source_name", "source_file", "bulletin_period", "load_timestamp"]
    ]
    out = out[keep_cols]

    if "country_name" not in out.columns:
        out["country_name"] = "Azerbaijan"
    if "country_iso" not in out.columns:
        out["country_iso"] = "AZE"

    out["period_type"] = _normalize_period_type(out["period_type"])
    return out


def _prep_periodic(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["period_date"] = pd.to_datetime(out["period_date"], errors="coerce")

    if "period_type" in out.columns:
        out["period_type"] = _normalize_period_type(out["period_type"])
    else:
        out["period_type"] = "month"

    keep_cols = [
        c for c in out.columns
        if c not in ["source_name", "source_file", "bulletin_period", "load_timestamp"]
    ]
    out = out[keep_cols]

    if "country_name" not in out.columns:
        out["country_name"] = "Azerbaijan"
    if "country_iso" not in out.columns:
        out["country_iso"] = "AZE"

    return out


def build_aze_digital_finance_periodic(
    national_payment_systems_df: pd.DataFrame,
    payment_service_df: pd.DataFrame,
    card_transactions_df: pd.DataFrame,
    customer_accounts_ebanking_df: pd.DataFrame,
    source_name: str = AZE_DIGITAL_FINANCE_SOURCE_NAME,
) -> pd.DataFrame:
    final_df = _prep_periodic(national_payment_systems_df)

    for df in [payment_service_df, card_transactions_df, customer_accounts_ebanking_df]:
        final_df = safe_merge_periodic(final_df, _to_periodic_month(df))

    final_df = (
        final_df
        .dropna(subset=["period_date"])
        .sort_values(["country_iso", "period_date", "period_type"])
        .drop_duplicates(subset=["country_iso", "period_date", "period_type"], keep="last")
        .reset_index(drop=True)
    )

    final_df["source_name"] = source_name
    final_df["load_timestamp"] = pd.Timestamp.utcnow()
    return final_df