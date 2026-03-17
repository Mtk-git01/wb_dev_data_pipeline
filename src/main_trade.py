from pathlib import Path

from src.config import (
    PROJECT_ID,
    DATASET_ID,
    TRADE_TABLE_COUNTRY_YEAR,
    TRADE_TABLE_COUNTRY_LATEST,
)
from src.extract_trade import fetch_all_trade_data
from src.transform_trade import transform_trade_long, latest_trade_snapshot
from src.validate import validate_country_year_table, print_validation_results
from src.load_bigquery import upload_to_bigquery


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = fetch_all_trade_data()
    print(raw_df.head(3))
    print(raw_df.columns.tolist())
    print(raw_df.shape)
    country_year_df = transform_trade_long(raw_df)
    print(country_year_df.head(3))
    print(country_year_df.shape)
    latest_df = latest_trade_snapshot(country_year_df)

    country_year_df.to_csv(output_dir / "trade_country_year_long.csv", index=False)
    latest_df.to_csv(output_dir / "trade_country_latest.csv", index=False)

    # validate
    trade_validate_df = country_year_df.rename(columns={
        "reporter_name": "country_name",
        "reporter_iso3": "country_iso",
    })
    latest_validate_df = latest_df.rename(columns={
        "reporter_name": "country_name",
        "reporter_iso3": "country_iso",
    })

    errors_year, warnings_year = validate_country_year_table(trade_validate_df)
    print_validation_results(errors_year, warnings_year, "trade_country_year_long")

    errors_latest, warnings_latest = validate_country_year_table(latest_validate_df)
    print_validation_results(errors_latest, warnings_latest, "trade_country_latest")

    if errors_year or errors_latest:
        raise ValueError("Validation failed for trade tables")

    upload_to_bigquery(
        country_year_df,
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id=TRADE_TABLE_COUNTRY_YEAR,
    )

    upload_to_bigquery(
        latest_df,
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id=TRADE_TABLE_COUNTRY_LATEST,
    )
    print("RAW SHAPE:", raw_df.shape)
    print(raw_df.head(3))

    print("TRANSFORMED SHAPE:", country_year_df.shape)
    print(country_year_df.head(3))

    print("LATEST SHAPE:", latest_df.shape)
    print(latest_df.head(3))


if __name__ == "__main__":
    main()