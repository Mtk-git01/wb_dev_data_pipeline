from pathlib import Path

from src.config import PROJECT_ID, EXTERNAL_DATASET_ID, U5MR_TABLE_ID, U5MR_URL
from src.extract_u5mr import load_u5mr_data
from src.transform_u5mr import prepare_all_countries_u5mr
from src.load_bigquery import upload_to_bigquery
from src.validate import validate_country_year_table, print_validation_results


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = load_u5mr_data(U5MR_URL)
    final_df = prepare_all_countries_u5mr(raw_df)

    print(final_df.head())
    print(final_df.shape)

    output_path = output_dir / "u5mr_country_year_all_countries.csv"
    final_df.to_csv(output_path, index=False)
    print(f"Saved local CSV: {output_path}")

    errors, warnings = validate_country_year_table(final_df)
    print_validation_results(errors, warnings, "u5mr_country_year")

    if errors:
        raise ValueError("Validation failed for u5mr_country_year")

    upload_to_bigquery(
        final_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=U5MR_TABLE_ID,
    )


if __name__ == "__main__":
    main()