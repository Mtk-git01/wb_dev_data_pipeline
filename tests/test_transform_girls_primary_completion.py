import pandas as pd

from src.transform_girls_primary_completion import transform_wb_indicator, latest_non_null


def test_transform_wb_indicator_basic():
    raw = pd.DataFrame({
        "country": [{"value": "Kazakhstan"}],
        "countryiso3code": ["KAZ"],
        "indicator": [{"value": "Primary completion rate, female (% of relevant age group)"}],
        "date": ["2023"],
        "value": ["88.5"],
        "obs_status": [""],
        "decimal": ["1"],
    })

    result = transform_wb_indicator(raw)

    assert result["country_name"].iloc[0] == "Kazakhstan"
    assert result["country_iso"].iloc[0] == "KAZ"
    assert int(result["year"].iloc[0]) == 2023
    assert float(result["value"].iloc[0]) == 88.5


def test_latest_non_null_picks_latest_value():
    df = pd.DataFrame({
        "country_name": ["Kazakhstan", "Kazakhstan", "Kazakhstan"],
        "country_iso": ["KAZ", "KAZ", "KAZ"],
        "year": [2021, 2022, 2023],
        "value": [85.0, None, 88.5],
        "indicator_code": ["SE.PRM.CMPT.FE.ZS"] * 3,
    })

    latest = latest_non_null(df)

    assert len(latest) == 1
    assert latest["year"].iloc[0] == 2023
    assert latest["value"].iloc[0] == 88.5