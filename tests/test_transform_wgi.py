import pandas as pd

from src.transform_wgi import transform_wgi, latest_non_null


def test_transform_wgi_basic():
    raw_df = pd.DataFrame({
        "country_name": ["Japan", "Japan", "Azerbaijan", "Azerbaijan"],
        "country_code": ["JPN", "JPN", "AZE", "AZE"],
        "indicator_code": ["GE.EST", "RQ.EST", "GE.EST", "RQ.EST"],
        "2023": [1.5, 1.4, -0.2, -0.4],
        "2024": [1.6, 1.5, -0.1, -0.3],
    })

    out = transform_wgi(raw_df)

    assert "government_effectiveness" in out.columns
    assert "regulatory_quality" in out.columns
    assert len(out) == 4


def test_latest_non_null_wgi():
    df = pd.DataFrame({
        "country_name": ["Japan", "Japan", "Azerbaijan"],
        "country_iso": ["JPN", "JPN", "AZE"],
        "year": [2023, 2024, 2024],
        "government_effectiveness": [1.5, 1.6, -0.1],
        "source_name": ["World Bank Worldwide Governance Indicators"] * 3,
        "load_timestamp": [pd.Timestamp("2026-03-21")] * 3,
    })

    latest = latest_non_null(df)

    assert len(latest) == 2
    assert latest.loc[latest["country_iso"] == "JPN", "year"].iloc[0] == 2024