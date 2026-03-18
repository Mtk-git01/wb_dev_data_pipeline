import pandas as pd

from src.transform_lays import transform_wb_indicator, latest_non_null


def test_transform_wb_indicator_basic():
    raw = pd.DataFrame({
        "country": [{"value": "Japan"}],
        "countryiso3code": ["JPN"],
        "indicator": [{"value": "Learning-adjusted years of schooling"}],
        "date": ["2020"],
        "value": ["12.3"],
        "obs_status": [""],
        "decimal": ["1"],
    })

    result = transform_wb_indicator(raw)

    assert result["country_name"].iloc[0] == "Japan"
    assert result["country_iso"].iloc[0] == "JPN"
    assert int(result["year"].iloc[0]) == 2020
    assert float(result["value"].iloc[0]) == 12.3


def test_latest_non_null_picks_latest_value():
    df = pd.DataFrame({
        "country_name": ["Japan", "Japan", "Japan"],
        "country_iso": ["JPN", "JPN", "JPN"],
        "year": [2018, 2019, 2020],
        "value": [11.8, None, 12.3],
        "indicator_code": ["HD.HCI.LAYS"] * 3,
    })

    latest = latest_non_null(df)

    assert len(latest) == 1
    assert latest["year"].iloc[0] == 2020
    assert latest["value"].iloc[0] == 12.3