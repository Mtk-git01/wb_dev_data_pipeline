import pandas as pd

from src.transform_big_mac import transform_big_mac, latest_non_null


def test_transform_big_mac_basic():
    raw = pd.DataFrame({
        "date": ["2025-01-01"],
        "iso_a3": ["JPN"],
        "name": ["Japan"],
        "currency_code": ["JPY"],
        "local_price": [480.0],
        "dollar_price": [3.2],
        "USD_raw": [-12.5],
        "USD_adjusted": [-5.0],
        "GDP_dollar": [33834.39],
    })

    result = transform_big_mac(raw)

    assert result["country_name"].iloc[0] == "Japan"
    assert result["country_iso"].iloc[0] == "JPN"
    assert int(result["year"].iloc[0]) == 2025
    assert float(result["dollar_price"].iloc[0]) == 3.2


def test_latest_non_null_picks_latest():
    df = pd.DataFrame({
        "country_name": ["Japan", "Japan"],
        "country_iso": ["JPN", "JPN"],
        "date": pd.to_datetime(["2024-07-01", "2025-01-01"]),
        "year": [2024, 2025],
        "dollar_price": [3.1, 3.2],
    })

    latest = latest_non_null(df)

    assert len(latest) == 1
    assert latest["year"].iloc[0] == 2025
    assert latest["dollar_price"].iloc[0] == 3.2