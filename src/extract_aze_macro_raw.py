from pathlib import Path
import pandas as pd

from src.config import AZE_MACRO_MONTHLY_RAW_PATH


def load_aze_macro_monthly_raw() -> pd.DataFrame:
    raw_path = Path(AZE_MACRO_MONTHLY_RAW_PATH)

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Azerbaijan macro raw file not found: {raw_path}. "
            "Create aze_macro_monthly.csv in data/raw/."
        )

    df = pd.read_csv(raw_path)
    if df.empty:
        raise ValueError("Azerbaijan macro raw CSV is empty")

    return df