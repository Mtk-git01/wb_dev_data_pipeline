import pandas as pd

import pandas as pd
from src.transform_global_findex import transform_global_findex, latest_non_null

def test_transform_global_findex_basic():
    raw_df = pd.DataFrame({
        "countrynewwb": ["Japan", "Japan", "Azerbaijan"],
        "codewb": ["JPN", "JPN", "AZE"],
        "year": [2021, 2024, 2021],
        "account_t_d": [95.0, 97.0, 63.0],
        "fiaccount_t_d": [94.0, 96.0, 61.0],
        "mobileaccount_t_d": [2.0, 3.0, None],
        "dig_acc": [88.0, 91.0, None],
        "borrow_any_t_d": [10.0, 11.0, 7.0],
    })

    out = transform_global_findex(raw_df)

    assert "country_name" in out.columns
    assert "country_iso" in out.columns
    assert "account_ownership_pct" in out.columns
    assert "digital_payment_pct" in out.columns
    assert len(out) == 3

def test_latest_non_null():
    df = pd.DataFrame({
        "country_name": ["Japan", "Japan", "Azerbaijan"],
        "country_iso": ["JPN", "JPN", "AZE"],
        "year": [2021, 2024, 2021],
        "account_ownership_pct": [95.0, 97.0, 63.0],
        "digital_payment_pct": [88.0, 91.0, 42.0],
        "source_name": ["World Bank Global Findex"] * 3,
        "load_timestamp": [pd.Timestamp("2026-03-21")] * 3,
    })

    latest = latest_non_null(df)

    assert len(latest) == 2
    assert latest.loc[latest["country_iso"] == "JPN", "year"].iloc[0] == 2024
    