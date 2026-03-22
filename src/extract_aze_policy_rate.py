from pathlib import Path
import pandas as pd

from src.config import AZE_POLICY_RATE_RAW_PATH


def load_aze_policy_rate_events() -> pd.DataFrame:
    """
    Load manually maintained CBAR policy-rate event table.

    Expected columns:
    - effective_date
    - refinancing_rate
    - corridor_floor
    - corridor_ceiling
    - source_url
    """
    raw_path = Path(AZE_POLICY_RATE_RAW_PATH)

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Policy rate raw file not found: {raw_path}. "
            "Create cbar_policy_rate_events.csv in data/raw/."
        )

    df = pd.read_csv(raw_path)
    if df.empty:
        raise ValueError("Policy rate raw CSV is empty")

    return df