import pandas as pd

from src.transform_city_temperature import add_city_metadata, annualize_city_temperature


def test_annualize_city_temperature_basic():
    raw = pd.DataFrame({
        "date": ["2023-01-01", "2023-01-02", "2023-12-31"],
        "temperature_2m_mean": [10.0, 12.0, 8.0],
    })

    raw = add_city_metadata(
        raw,
        city_name="Tokyo",
        country_name="Japan",
        latitude=35.6762,
        longitude=139.6503,
    )

    annual = annualize_city_temperature(raw)

    assert len(annual) == 1
    assert annual["city_name"].iloc[0] == "Tokyo"
    assert int(annual["year"].iloc[0]) == 2023
    assert round(float(annual["avg_temp_c_annual"].iloc[0]), 2) == 10.00
    assert int(annual["observation_days"].iloc[0]) == 3