from pathlib import Path
from datetime import date

from src.config import (
    PROJECT_ID,
    AZE_BRONZE_DATASET_ID,
    AZE_SILVER_DATASET_ID,
    AZE_MACRO_MONTHLY_RAW_TABLE,
    AZE_MACRO_MONTHLY_TABLE,
)
from src.extract_aze_cb_ar_macro_api import fetch_aze_fx_reserves_range
from src.extract_aze_ssc_cpi_api import fetch_aze_cpi_range
from src.transform_aze_macro_monthly import build_aze_macro_monthly
from src.load_bigquery import upload_to_bigquery


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    this_year = date.today().year

    reserves_raw = fetch_aze_fx_reserves_range(start_year=2024, end_year=this_year)
    cpi_raw = fetch_aze_cpi_range(max_pages=36)

    # Bronze macro raw is the merged source-near raw landing
    bronze_raw = reserves_raw.merge(cpi_raw, on="month", how="outer", suffixes=("_reserves", "_cpi"))

    silver_df = build_aze_macro_monthly(
        cpi_df=cpi_raw,
        reserves_df=reserves_raw,
    )

    bronze_raw.to_csv(output_dir / "aze_macro_monthly_raw_api.csv", index=False)
    silver_df.to_csv(output_dir / "aze_macro_monthly.csv", index=False)

    upload_to_bigquery(
        bronze_raw,
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