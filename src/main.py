from pathlib import Path

from src.config import PROJECT_ID, DATASET_ID, TABLE_ID, U5MR_URL
from src.extract import load_u5mr_data
from src.transform import prepare_all_countries_u5mr
from src.load_bigquery import upload_u5mr_to_bigquery


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

    upload_u5mr_to_bigquery(
        final_df,
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id=TABLE_ID,
    )


if __name__ == "__main__":
    main()