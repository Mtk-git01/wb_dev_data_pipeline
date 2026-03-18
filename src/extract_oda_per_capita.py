import requests
import pandas as pd

from src.config import WB_API_BASE, ODA_PER_CAPITA_INDICATOR_CODE


def fetch_all_countries_metadata() -> pd.DataFrame:
    url = f"{WB_API_BASE}/country?format=json&per_page=400"
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    payload = r.json()

    if len(payload) < 2:
        raise ValueError("Unexpected API response for country metadata.")

    return pd.DataFrame(payload[1])


def get_world_countries_only() -> pd.DataFrame:
    meta = fetch_all_countries_metadata().copy()

    meta["region_name"] = meta["region"].apply(
        lambda x: x["value"] if isinstance(x, dict) else None
    )

    countries = meta[
        (meta["region_name"].notna()) &
        (meta["region_name"] != "Aggregates")
    ].copy()

    countries = countries.rename(columns={"id": "country_code_api"})
    return countries[["country_code_api", "name", "iso2Code", "region_name"]]


def fetch_indicator_for_countries(country_codes: list[str]) -> pd.DataFrame:
    joined = ";".join(country_codes)

    url = (
        f"{WB_API_BASE}/country/{joined}/indicator/{ODA_PER_CAPITA_INDICATOR_CODE}"
        f"?format=json&per_page=30000"
    )

    r = requests.get(url, timeout=60)
    r.raise_for_status()
    payload = r.json()

    if len(payload) < 2:
        raise ValueError("Unexpected API response for indicator data.")

    return pd.DataFrame(payload[1])