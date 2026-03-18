from pathlib import Path
import pandas as pd

from src.config import (
    PROJECT_ID,
    EXTERNAL_DATASET_ID,
    CITY_TEMP_TABLE_ANNUAL,
    CITY_TEMPERATURE_CITIES,
)
from src.extract_city_temperature import fetch_city_daily_temperature
from src.transform_city_temperature import add_city_metadata, annualize_city_temperature
from src.load_bigquery import upload_to_bigquery


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    all_annual = []

    for city in CITY_TEMPERATURE_CITIES:
        city_name = city["city_name"]
        country_name = city["country_name"]
        latitude = city["latitude"]
        longitude = city["longitude"]

        print(f"Fetching daily temperature for {city_name}, {country_name}...")

        daily_df = fetch_city_daily_temperature(latitude=latitude, longitude=longitude)
        daily_df = add_city_metadata(
            daily_df,
            city_name=city_name,
            country_name=country_name,
            latitude=latitude,
            longitude=longitude,
        )

        annual_df = annualize_city_temperature(daily_df)
        all_annual.append(annual_df)

    final_df = pd.concat(all_annual, ignore_index=True)

    final_df.to_csv(
        output_dir / "city_temperature_annual.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(final_df.head())
    print(final_df.shape)

    upload_to_bigquery(
        final_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=CITY_TEMP_TABLE_ANNUAL,
    )


if __name__ == "__main__":
    main()