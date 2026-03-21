from pathlib import Path

from src.config import (
    PROJECT_ID,
    EXTERNAL_DATASET_ID,
    IMF_FAS_TABLE_COUNTRY_YEAR,
    IMF_FAS_TABLE_COUNTRY_LATEST,
)
from src.extract_imf_fas import load_imf_fas_raw
from src.transform_imf_fas import transform_imf_fas, latest_non_null
from src.validate import validate_country_year_table, print_validation_results
from src.load_bigquery import upload_to_bigquery


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = load_imf_fas_raw()
    country_year_df = transform_imf_fas(raw_df)
    country_latest_df = latest_non_null(country_year_df)

    country_year_df.to_csv(
        output_dir / "imf_fas_country_year.csv",
        index=False
    )
    country_latest_df.to_csv(
        output_dir / "imf_fas_country_latest.csv",
        index=False
    )

    errors_year, warnings_year = validate_country_year_table(country_year_df)
    print_validation_results(errors_year, warnings_year, "imf_fas_country_year")

    errors_latest, warnings_latest = validate_country_year_table(country_latest_df)
    print_validation_results(errors_latest, warnings_latest, "imf_fas_country_latest")

    if errors_year or errors_latest:
        raise ValueError("Validation failed for IMF FAS tables")

    upload_to_bigquery(
        country_year_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=IMF_FAS_TABLE_COUNTRY_YEAR,
    )

    upload_to_bigquery(
        country_latest_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=IMF_FAS_TABLE_COUNTRY_LATEST,
    )


if __name__ == "__main__":
    main()