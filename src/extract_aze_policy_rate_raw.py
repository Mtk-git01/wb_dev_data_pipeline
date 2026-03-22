from pathlib import Path
import pandas as pd

from src.config import AZE_POLICY_RATE_RAW_PATH


def load_aze_policy_rate_events_raw() -> pd.DataFrame:
    raw_path = Path(AZE_POLICY_RATE_RAW_PATH)

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Azerbaijan policy-rate raw file not found: {raw_path}. "
            "Create cbar_policy_rate_events.csv in data/raw/."
        )

    df = pd.read_csv(raw_path)
    if df.empty:
        raise ValueError("Azerbaijan policy-rate raw CSV is empty")

    return df