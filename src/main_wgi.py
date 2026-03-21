from pathlib import Path

from src.config import (
    PROJECT_ID,
    DATASET_ID,
    WGI_TABLE_COUNTRY_YEAR,
    WGI_TABLE_COUNTRY_LATEST,
)
from src.extract_wgi import load_wgi_raw
from src.transform_wgi import transform_wgi, latest_non_null
from src.validate import validate_country_year_table, print_validation_results
from src.load_bigquery import upload_to_bigquery


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = load_wgi_raw()
    country_year_df = transform_wgi(raw_df)
    country_latest_df = latest_non_null(country_year_df)

    country_year_df.to_csv(
        output_dir / "wgi_country_year.csv",
        index=False
    )
    country_latest_df.to_csv(
        output_dir / "wgi_country_latest.csv",
        index=False
    )

    errors_year, warnings_year = validate_country_year_table(country_year_df)
    print_validation_results(errors_year, warnings_year, "wgi_country_year")

    errors_latest, warnings_latest = validate_country_year_table(country_latest_df)
    print_validation_results(errors_latest, warnings_latest, "wgi_country_latest")

    if errors_year or errors_latest:
        raise ValueError("Validation failed for WGI tables")

    upload_to_bigquery(
        country_year_df,
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id=WGI_TABLE_COUNTRY_YEAR,
    )

    upload_to_bigquery(
        country_latest_df,
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id=WGI_TABLE_COUNTRY_LATEST,
    )


if __name__ == "__main__":
    main()