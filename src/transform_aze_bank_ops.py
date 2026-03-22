import pandas as pd


def transform_aze_policy_rate_monthly(policy_df: pd.DataFrame) -> pd.DataFrame:
    df = policy_df.copy()

    required = ["effective_date", "refinancing_rate", "corridor_floor", "corridor_ceiling"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing policy-rate columns: {missing}")

    df["effective_date"] = pd.to_datetime(df["effective_date"], errors="coerce")
    df["refinancing_rate"] = pd.to_numeric(df["refinancing_rate"], errors="coerce")
    df["corridor_floor"] = pd.to_numeric(df["corridor_floor"], errors="coerce")
    df["corridor_ceiling"] = pd.to_numeric(df["corridor_ceiling"], errors="coerce")

    df = df.dropna(subset=["effective_date"]).sort_values("effective_date").copy()

    start_month = df["effective_date"].min().to_period("M").to_timestamp()
    end_month = pd.Timestamp.today().to_period("M").to_timestamp()

    monthly_index = pd.DataFrame({
        "month": pd.date_range(start=start_month, end=end_month, freq="MS")
    })

    df["month"] = df["effective_date"].dt.to_period("M").dt.to_timestamp()

    monthly = monthly_index.merge(
        df[["month", "refinancing_rate", "corridor_floor", "corridor_ceiling"]],
        on="month",
        how="left"
    ).sort_values("month")

    monthly[["refinancing_rate", "corridor_floor", "corridor_ceiling"]] = (
        monthly[["refinancing_rate", "corridor_floor", "corridor_ceiling"]].ffill()
    )

    return monthly


def load_and_validate_aze_banking_monthly(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()

    required = [
        "month",
        "cpi_yoy",
        "official_fx_reserves_usd_mn",
        "bank_total_assets_mn_azn",
        "bank_loans_customers_mn_azn",
        "bank_deposits_total_mn_azn",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing banking monthly columns: {missing}")

    df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.to_period("M").dt.to_timestamp()

    numeric_cols = [
        "cpi_yoy",
        "official_fx_reserves_usd_mn",
        "bank_total_assets_mn_azn",
        "bank_loans_customers_mn_azn",
        "bank_deposits_total_mn_azn",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["month"]).sort_values("month").drop_duplicates(subset=["month"])
    return df.reset_index(drop=True)


def build_aze_fx_monthly_from_daily(fx_daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert daily FX snapshots into monthly table using latest observation in each month.
    """
    df = fx_daily_df.copy()

    required = ["as_of_date", "currency_code", "rate_azn_per_unit"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing FX daily columns: {missing}")

    df["as_of_date"] = pd.to_datetime(df["as_of_date"], errors="coerce")
    df["month"] = df["as_of_date"].dt.to_period("M").dt.to_timestamp()
    df["rate_azn_per_unit"] = pd.to_numeric(df["rate_azn_per_unit"], errors="coerce")

    df = df.dropna(subset=["as_of_date", "currency_code", "rate_azn_per_unit"]).copy()

    # latest observation within each month / currency
    df = (
        df.sort_values(["currency_code", "as_of_date"])
          .groupby(["month", "currency_code"], as_index=False)
          .tail(1)
    )

    wide = df.pivot_table(
        index="month",
        columns="currency_code",
        values="rate_azn_per_unit",
        aggfunc="first"
    ).reset_index()

    rename_map = {c: f"{c.lower()}_azn" for c in wide.columns if c != "month"}
    wide = wide.rename(columns=rename_map)

    return wide.sort_values("month").reset_index(drop=True)


def build_aze_bank_ops_monthly(
    fx_monthly_df: pd.DataFrame,
    policy_monthly_df: pd.DataFrame,
    banking_monthly_df: pd.DataFrame,
    source_name: str,
) -> pd.DataFrame:
    df = banking_monthly_df.merge(policy_monthly_df, on="month", how="left")
    df = df.merge(fx_monthly_df, on="month", how="left")

    df["source_name"] = source_name
    df["load_timestamp"] = pd.Timestamp.utcnow()

    return df.sort_values("month").reset_index(drop=True)