from pathlib import Path

from src.config import (
    PROJECT_ID,
    AZE_BRONZE_DATASET_ID,
    AZE_SILVER_DATASET_ID,
    AZE_MACRO_MONTHLY_RAW_TABLE,
    AZE_MACRO_MONTHLY_TABLE,
)
from src.extract_aze_macro_raw import load_aze_macro_monthly_raw
from src.transform_aze_macro_monthly import transform_aze_macro_monthly
from src.load_bigquery import upload_to_bigquery


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = load_aze_macro_monthly_raw()
    silver_df = transform_aze_macro_monthly(raw_df)

    raw_df.to_csv(output_dir / "aze_macro_monthly_raw.csv", index=False)
    silver_df.to_csv(output_dir / "aze_macro_monthly.csv", index=False)

    upload_to_bigquery(
        raw_df,
        project_id=PROJECT_ID,
        dataset_id=AZE_BRONZE_DATASET_ID,
        table_id=AZE_MACRO_MONTHLY_RAW_TABLE,
    )

    upload_to_bigquery(
        silver_df,
        project_id=PROJECT_ID,
        dataset_id=AZE_SILVER_DATASET_ID,
        table_id=AZE_MACRO_MONTHLY_TABLE,
    )


if __name__ == "__main__":
    main()