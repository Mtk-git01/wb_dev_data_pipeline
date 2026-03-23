
import pandas as pd
from src.config import AZE_CREDIT_ACCESS_AND_STABILITY_SOURCE_NAME
from src.extract_aze_bulletin_common import safe_merge_periodic

def _prep(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["period_date"] = pd.to_datetime(out["period_date"], errors="coerce")
    for col in out.columns:
        if col not in ["country_name","country_iso","period_date","period_type","source_name","source_file","bulletin_period","load_timestamp"]:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    keep_cols = [c for c in out.columns if c not in ["source_name","source_file","bulletin_period","load_timestamp"]]
    return out[keep_cols]

def build_aze_credit_access_and_stability_periodic(
    business_portfolio_df: pd.DataFrame,
    sectoral_loans_df: pd.DataFrame,
    npl_structure_df: pd.DataFrame,
    interest_rates_df: pd.DataFrame,
    movable_registry_df: pd.DataFrame,
    source_name: str = AZE_CREDIT_ACCESS_AND_STABILITY_SOURCE_NAME,
) -> pd.DataFrame:
    final_df = _prep(business_portfolio_df)
    for df in [sectoral_loans_df, npl_structure_df, interest_rates_df, movable_registry_df]:
        final_df = safe_merge_periodic(final_df, _prep(df))

    final_df = final_df.sort_values(["country_iso","period_date","period_type"]).drop_duplicates(
        subset=["country_iso","period_date","period_type"], keep="last"
    ).reset_index(drop=True)
    final_df["source_name"] = source_name
    final_df["load_timestamp"] = pd.Timestamp.utcnow()
    return final_df
