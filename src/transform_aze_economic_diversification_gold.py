
import pandas as pd
from src.config import AZE_ECONOMIC_DIVERSIFICATION_SOURCE_NAME
from src.extract_aze_bulletin_common import safe_merge_periodic

def _prep(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["period_date"] = pd.to_datetime(out["period_date"], errors="coerce")
    keep_cols = [c for c in out.columns if c not in ["source_name","source_file","bulletin_period","load_timestamp"]]
    return out[keep_cols]

def build_aze_economic_diversification_periodic(
    macro_main_df: pd.DataFrame,
    balance_of_payments_df: pd.DataFrame,
    foreign_trade_df: pd.DataFrame,
    source_name: str = AZE_ECONOMIC_DIVERSIFICATION_SOURCE_NAME,
) -> pd.DataFrame:
    final_df = _prep(macro_main_df)
    for df in [balance_of_payments_df, foreign_trade_df]:
        final_df = safe_merge_periodic(final_df, _prep(df))
    final_df = final_df.sort_values(["country_iso","period_date","period_type"]).drop_duplicates(
        subset=["country_iso","period_date","period_type"], keep="last"
    ).reset_index(drop=True)
    final_df["source_name"] = source_name
    final_df["load_timestamp"] = pd.Timestamp.utcnow()
    return final_df
