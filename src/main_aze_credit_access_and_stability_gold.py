
from pathlib import Path
import pandas as pd
from google.cloud import bigquery

from src.config import PROJECT_ID, EXTERNAL_DATASET_ID, AZE_SILVER_DATASET_ID, AZE_CREDIT_ACCESS_AND_STABILITY_TABLE, AZE_CREDIT_ACCESS_AND_STABILITY_SOURCE_NAME, AZE_BUSINESS_PORTFOLIO_PERIODIC_TABLE, AZE_SECTORAL_LOANS_PERIODIC_TABLE, AZE_NPL_STRUCTURE_PERIODIC_TABLE, AZE_INTEREST_RATES_PERIODIC_TABLE, AZE_MOVABLE_PROPERTY_REGISTRY_PERIODIC_TABLE
from src.load_bigquery import upload_to_bigquery
from src.transform_aze_credit_access_and_stability_gold import build_aze_credit_access_and_stability_periodic


def read_table_from_bigquery(project_id: str, dataset_id: str, table_id: str) -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    return client.query(query).to_dataframe()


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    business_portfolio_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_BUSINESS_PORTFOLIO_PERIODIC_TABLE)
    sectoral_loans_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_SECTORAL_LOANS_PERIODIC_TABLE)
    npl_structure_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_NPL_STRUCTURE_PERIODIC_TABLE)
    interest_rates_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_INTEREST_RATES_PERIODIC_TABLE)
    movable_registry_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_MOVABLE_PROPERTY_REGISTRY_PERIODIC_TABLE)

    final_df = build_aze_credit_access_and_stability_periodic(
        business_portfolio_df=business_portfolio_df,
        sectoral_loans_df=sectoral_loans_df,
        npl_structure_df=npl_structure_df,
        interest_rates_df=interest_rates_df,
        movable_registry_df=movable_registry_df,
        source_name=AZE_CREDIT_ACCESS_AND_STABILITY_SOURCE_NAME,
    )

    final_df.to_csv(output_dir / "aze_credit_access_and_stability_periodic.csv", index=False)

    upload_to_bigquery(
        final_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=AZE_CREDIT_ACCESS_AND_STABILITY_TABLE,
    )


if __name__ == "__main__":
    main()
