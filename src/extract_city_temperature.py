import requests
import pandas as pd

from src.config import (
    CITY_TEMPERATURE_MODEL,
    CITY_TEMP_START_DATE,
    CITY_TEMP_END_DATE,
)


def fetch_city_daily_temperature(latitude: float, longitude: float) -> pd.DataFrame:
    """
    Open-Meteo Historical Weather API から daily mean temperature を取得する。
    """
    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": CITY_TEMP_START_DATE,
        "end_date": CITY_TEMP_END_DATE,
        "daily": "temperature_2m_mean",
        "timezone": "GMT",
        "models": CITY_TEMPERATURE_MODEL,
    }

    r = requests.get(url, params=params, timeout=120)
    r.raise_for_status()
    payload = r.json()

    if "daily" not in payload:
        raise ValueError("Unexpected Open-Meteo response: missing 'daily'.")

    daily = payload["daily"]

    if "time" not in daily or "temperature_2m_mean" not in daily:
        raise ValueError("Unexpected Open-Meteo response: missing daily fields.")

    df = pd.DataFrame({
        "date": daily["time"],
        "temperature_2m_mean": daily["temperature_2m_mean"],
    })

    return df