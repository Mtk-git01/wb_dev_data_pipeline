import pandas as pd

import pandas as pd
from src.transform_imf_fas import transform_imf_fas, latest_non_null

def test_transform_imf_fas_basic():
    raw_df = pd.DataFrame({
        "COUNTRY": ["Belgium", "Belgium", "Belgium"],
        "SERIES_CODE": [
            "BEL.FA21_COMBANK.NUM.A",
            "BEL.COMBANK.NUM.A",
            "BEL.FA63.NUM.A",
        ],
        "INDICATOR": [
            "Borrowers, Commercial banks",
            "Commercial banks",
            "Active mobile money accounts",
        ],
        "2023": [6496149, 100, 250000],
        "2024": [6500000, 101, 255000],
    })

    out = transform_imf_fas(raw_df)

    assert "country_name" in out.columns
    assert "country_iso" in out.columns
    assert "borrowers_commercial_banks_number" in out.columns
    assert "commercial_banks_number" in out.columns
    assert "active_mobile_money_accounts_number" in out.columns
    assert len(out) == 2


def test_latest_non_null():
    df = pd.DataFrame({
        "country_name": ["Belgium", "Belgium"],
        "country_iso": ["BEL", "BEL"],
        "year": [2023, 2024],
        "borrowers_commercial_banks_number": [6496149, 6500000],
        "source_name": ["IMF Financial Access Survey", "IMF Financial Access Survey"],
        "load_timestamp": [pd.Timestamp("2026-03-21"), pd.Timestamp("2026-03-21")],
    })

    latest = latest_non_null(df)
    assert len(latest) == 1
    assert latest.iloc[0]["year"] == 2024