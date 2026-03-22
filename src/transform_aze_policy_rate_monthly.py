import pandas as pd

from src.config import AZE_POLICY_RATE_SOURCE_NAME


def transform_aze_policy_rate_monthly(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()

    required = [
        "month",
        "corridor_floor",
        "refinancing_rate",
        "corridor_ceiling",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing Azerbaijan policy monthly columns: {missing}")

    df["month"] = pd.to_datetime(df["month"], errors="coerce").dt.to_period("M").dt.to_timestamp()

    for col in ["corridor_floor", "refinancing_rate", "corridor_ceiling"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = (
        df.dropna(subset=["month"])
        .sort_values("month")
        .drop_duplicates(subset=["month"], keep="last")
        .reset_index(drop=True)
    )

    df["source_name"] = AZE_POLICY_RATE_SOURCE_NAME
    df["load_timestamp"] = pd.Timestamp.utcnow()

    return df