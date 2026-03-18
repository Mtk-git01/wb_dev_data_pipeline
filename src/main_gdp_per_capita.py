from pathlib import Path

from src.config import (
    PROJECT_ID,
    DATASET_ID,
    GDP_PC_TABLE_COUNTRY_YEAR,
    GDP_PC_TABLE_COUNTRY_LATEST,
)
from src.extract_gdp_per_capita import (
    get_world_countries_only,
    fetch_indicator_for_countries,
)
from src.transform_gdp_per_capita import (
    transform_wb_indicator,
    latest_non_null,
)
from src.validate import validate_country_year_table, print_validation_results
from src.load_bigquery import upload_to_bigquery


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    countries = get_world_countries_only()
    country_codes = countries["country_code_api"].dropna().tolist()

    raw_df = fetch_indicator_for_countries(country_codes)
    country_year_df = transform_wb_indicator(raw_df)
    country_latest_df = latest_non_null(country_year_df)

    country_year_df.to_csv(
        output_dir / "gdp_per_capita_country_year.csv",
        index=False
    )
    country_latest_df.to_csv(
        output_dir / "gdp_per_capita_country_latest.csv",
        index=False
    )

    errors_year, warnings_year = validate_country_year_table(country_year_df)
    print_validation_results(errors_year, warnings_year, "gdp_per_capita_country_year")

    errors_latest, warnings_latest = validate_country_year_table(country_latest_df)
    print_validation_results(errors_latest, warnings_latest, "gdp_per_capita_country_latest")

    if errors_year or errors_latest:
        raise ValueError("Validation failed for GDP per capita tables")

    upload_to_bigquery(
        country_year_df,
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id=GDP_PC_TABLE_COUNTRY_YEAR,
    )

    upload_to_bigquery(
        country_latest_df,
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id=GDP_PC_TABLE_COUNTRY_LATEST,
    )


if __name__ == "__main__":
    main()