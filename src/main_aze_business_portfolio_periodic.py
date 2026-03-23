
from pathlib import Path

from src.config import PROJECT_ID, AZE_BRONZE_DATASET_ID, AZE_SILVER_DATASET_ID, AZE_BUSINESS_PORTFOLIO_PERIODIC_RAW_TABLE, AZE_BUSINESS_PORTFOLIO_PERIODIC_TABLE
from src.extract_aze_business_portfolio_xlsx_raw import load_aze_business_portfolio_xlsx_raw
from src.transform_aze_business_portfolio_periodic import transform_aze_business_portfolio_periodic
from src.load_bigquery import upload_to_bigquery


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = load_aze_business_portfolio_xlsx_raw()
    silver_df = transform_aze_business_portfolio_periodic(raw_df)

    raw_df.to_csv(output_dir / "aze_business_portfolio_periodic_raw.csv", index=False)
    silver_df.to_csv(output_dir / "aze_business_portfolio_periodic.csv", index=False)

    upload_to_bigquery(
        raw_df,
        project_id=PROJECT_ID,
        dataset_id=AZE_BRONZE_DATASET_ID,
        table_id=AZE_BUSINESS_PORTFOLIO_PERIODIC_RAW_TABLE,
    )
    upload_to_bigquery(
        silver_df,
        project_id=PROJECT_ID,
        dataset_id=AZE_SILVER_DATASET_ID,
        table_id=AZE_BUSINESS_PORTFOLIO_PERIODIC_TABLE,
    )


if __name__ == "__main__":
    main()
