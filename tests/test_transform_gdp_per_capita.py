import pandas as pd

from src.transform_gdp_per_capita import transform_wb_indicator, latest_non_null


def test_transform_wb_indicator_basic():
    raw = pd.DataFrame({
        "country": [{"value": "Japan"}],
        "countryiso3code": ["JPN"],
        "indicator": [{"value": "GDP per capita (current US$)"}],
        "date": ["2023"],
        "value": ["33834.39"],
        "obs_status": [""],
        "decimal": ["2"],
    })

    result = transform_wb_indicator(raw)

    assert result["country_name"].iloc[0] == "Japan"
    assert result["country_iso"].iloc[0] == "JPN"
    assert int(result["year"].iloc[0]) == 2023
    assert float(result["value"].iloc[0]) == 33834.39


def test_latest_non_null_picks_latest_value():
    df = pd.DataFrame({
        "country_name": ["Japan", "Japan", "Japan"],
        "country_iso": ["JPN", "JPN", "JPN"],
        "year": [2021, 2022, 2023],
        "value": [39312.0, None, 33834.39],
        "indicator_code": ["NY.GDP.PCAP.CD"] * 3,
    })

    latest = latest_non_null(df)

    assert len(latest) == 1
    assert latest["year"].iloc[0] == 2023
    assert latest["value"].iloc[0] == 33834.39