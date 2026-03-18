import pandas as pd

from src.config import BIG_MAC_CSV_URL


def load_big_mac_data(url: str = BIG_MAC_CSV_URL) -> pd.DataFrame:
    df = pd.read_csv(url)
    return df