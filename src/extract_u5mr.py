import pandas as pd
import requests
from io import BytesIO


def load_u5mr_data(url: str) -> pd.DataFrame:
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    df = pd.read_excel(
        BytesIO(response.content),
        sheet_name="Total U5MR",
        skiprows=2
    )
    return df