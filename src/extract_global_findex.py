from pathlib import Path
import pandas as pd

from src.config import GLOBAL_FINDEX_RAW_PATH


def load_global_findex_raw() -> pd.DataFrame:
    """
    Load raw Global Findex country-level CSV from local landing path.

    Expected location:
        data/raw/global_findex_country.csv
    """
    raw_path = Path(GLOBAL_FINDEX_RAW_PATH)

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Global Findex raw file not found: {raw_path}. "
            "Download the official country-level CSV and place it there."
        )

    df = pd.read_csv(raw_path)
    if df.empty:
        raise ValueError("Global Findex raw file is empty")

    return df