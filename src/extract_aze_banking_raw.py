from pathlib import Path
import pandas as pd

from src.config import AZE_BANKING_MONTHLY_RAW_PATH


def load_aze_banking_monthly_raw() -> pd.DataFrame:
    raw_path = Path(AZE_BANKING_MONTHLY_RAW_PATH)

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Azerbaijan banking raw file not found: {raw_path}. "
            "Create aze_banking_monthly.csv in data/raw/."
        )

    df = pd.read_csv(raw_path)
    if df.empty:
        raise ValueError("Azerbaijan banking raw CSV is empty")

    return df