import pandas as pd
from datetime import datetime, timezone

from src.config import CITY_TEMPERATURE_SOURCE_NAME


def add_city_metadata(
    df: pd.DataFrame,
    city_name: str,
    country_name: str,
    latitude: float,
    longitude: float,
) -> pd.DataFrame:
    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out["year"] = out["date"].dt.year.astype("Int64")
    out["city_name"] = city_name
    out["country_name"] = country_name
    out["latitude"] = latitude
    out["longitude"] = longitude
    out["source_name"] = CITY_TEMPERATURE_SOURCE_NAME
    return out


def annualize_city_temperature(df: pd.DataFrame) -> pd.DataFrame:
    """
    daily mean temperature を city-year の年平均に集約する。
    """
    work = df.copy()

    work["temperature_2m_mean"] = pd.to_numeric(
        work["temperature_2m_mean"], errors="coerce"
    )

    annual = (
        work.groupby(
            ["city_name", "country_name", "year", "latitude", "longitude", "source_name"],
            as_index=False
        )
        .agg(
            avg_temp_c_annual=("temperature_2m_mean", "mean"),
            observation_days=("temperature_2m_mean", lambda s: s.notna().sum()),
        )
    )

    annual["load_timestamp"] = datetime.now(timezone.utc)

    annual = annual.sort_values(["city_name", "year"]).reset_index(drop=True)
    return annual