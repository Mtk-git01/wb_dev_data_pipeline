import pandas as pd


def build_aze_bank_ops_monthly(
    fx_monthly_df: pd.DataFrame,
    policy_monthly_df: pd.DataFrame,
    macro_monthly_df: pd.DataFrame,
    banking_monthly_df: pd.DataFrame,
    source_name: str,
) -> pd.DataFrame:
    fx = fx_monthly_df.copy()
    policy = policy_monthly_df.copy()
    macro = macro_monthly_df.copy()
    banking = banking_monthly_df.copy()

    for df in [fx, policy, macro, banking]:
        df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.to_period("M").dt.to_timestamp()

    # source/load columnsはGoldでは不要なので落とす
    drop_cols = ["source_name", "load_timestamp"]
    policy = policy.drop(columns=[c for c in drop_cols if c in policy.columns])
    macro = macro.drop(columns=[c for c in drop_cols if c in macro.columns])
    banking = banking.drop(columns=[c for c in drop_cols if c in banking.columns])

    df = macro.merge(policy, on="month", how="left")
    df = df.merge(banking, on="month", how="left")
    df = df.merge(fx, on="month", how="left")

    df["source_name"] = source_name
    df["load_timestamp"] = pd.Timestamp.utcnow()

    return df.sort_values("month").reset_index(drop=True)