import pandas as pd

from src.config import AZE_POLICY_RATE_SOURCE_NAME


def transform_aze_policy_rate_monthly(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Expected raw columns:
    - effective_date
    - refinancing_rate
    - corridor_floor
    - corridor_ceiling
    """
    df = raw_df.copy()

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

    monthly["source_name"] = AZE_POLICY_RATE_SOURCE_NAME
    monthly["load_timestamp"] = pd.Timestamp.utcnow()

    return monthly.reset_index(drop=True)