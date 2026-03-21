from pathlib import Path
import pandas as pd

from src.config import IMF_FAS_RAW_PATH


def load_imf_fas_raw() -> pd.DataFrame:
    raw_path = Path(IMF_FAS_RAW_PATH)

    if not raw_path.exists():
        raise FileNotFoundError(
            f"IMF FAS raw file not found: {raw_path}. "
            "Download/export the FAS CSV and place it there."
        )

    df = pd.read_csv(raw_path)
    if df.empty:
        raise ValueError("IMF FAS raw file is empty")

    return df