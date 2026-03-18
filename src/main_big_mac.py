from pathlib import Path

from src.config import (
    PROJECT_ID,
    EXTERNAL_DATASET_ID,
    BIG_MAC_TABLE_COUNTRY_PERIOD,
    BIG_MAC_TABLE_COUNTRY_LATEST,
    BIG_MAC_CSV_URL,
)
from src.extract_big_mac import load_big_mac_data
from src.transform_big_mac import transform_big_mac, latest_non_null
from src.validate import validate_country_year_table, print_validation_results
from src.load_bigquery import upload_to_bigquery


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = load_big_mac_data(BIG_MAC_CSV_URL)
    country_period_df = transform_big_mac(raw_df)
    country_latest_df = latest_non_null(country_period_df)

    country_period_df.to_csv(
        output_dir / "big_mac_index_country_period.csv",
        index=False
    )
    country_latest_df.to_csv(
        output_dir / "big_mac_index_country_latest.csv",
        index=False
    )

    # validate は year ベースで最低限流す
    validate_df = country_period_df.copy()
    errors_year, warnings_year = validate_country_year_table(validate_df)
    print_validation_results(errors_year, warnings_year, "big_mac_index_country_period")

    validate_latest_df = country_latest_df.copy()
    errors_latest, warnings_latest = validate_country_year_table(validate_latest_df)
    print_validation_results(errors_latest, warnings_latest, "big_mac_index_country_latest")

    if errors_year or errors_latest:
        raise ValueError("Validation failed for Big Mac Index tables")

    upload_to_bigquery(
        country_period_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=BIG_MAC_TABLE_COUNTRY_PERIOD,
    )

    upload_to_bigquery(
        country_latest_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=BIG_MAC_TABLE_COUNTRY_LATEST,
    )


if __name__ == "__main__":
    main()