from pathlib import Path
import pandas as pd

from src.config import WGI_RAW_PATH


def load_wgi_raw() -> pd.DataFrame:
    raw_path = Path(WGI_RAW_PATH)

    if not raw_path.exists():
        raise FileNotFoundError(
            f"WGI raw file not found: {raw_path}. "
            "Download the WGI Excel file and place it there."
        )

    df = pd.read_excel(raw_path, sheet_name=0, engine="openpyxl")

    if df.empty:
        raise ValueError("WGI raw file is empty")

    return df