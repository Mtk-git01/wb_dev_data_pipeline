
from pathlib import Path
import pandas as pd
from google.cloud import bigquery

from src.config import PROJECT_ID, EXTERNAL_DATASET_ID, AZE_SILVER_DATASET_ID, AZE_ECONOMIC_DIVERSIFICATION_TABLE, AZE_ECONOMIC_DIVERSIFICATION_SOURCE_NAME, AZE_MACRO_MAIN_PERIODIC_TABLE, AZE_BALANCE_OF_PAYMENTS_PERIODIC_TABLE, AZE_FOREIGN_TRADE_PERIODIC_TABLE
from src.load_bigquery import upload_to_bigquery
from src.transform_aze_economic_diversification_gold import build_aze_economic_diversification_periodic


def read_table_from_bigquery(project_id: str, dataset_id: str, table_id: str) -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    return client.query(query).to_dataframe()


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    macro_main_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_MACRO_MAIN_PERIODIC_TABLE)
    balance_of_payments_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_BALANCE_OF_PAYMENTS_PERIODIC_TABLE)
    foreign_trade_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_FOREIGN_TRADE_PERIODIC_TABLE)

    final_df = build_aze_economic_diversification_periodic(
        macro_main_df=macro_main_df,
        balance_of_payments_df=balance_of_payments_df,
        foreign_trade_df=foreign_trade_df,
        source_name=AZE_ECONOMIC_DIVERSIFICATION_SOURCE_NAME,
    )

    final_df.to_csv(output_dir / "aze_economic_diversification_periodic.csv", index=False)

    upload_to_bigquery(
        final_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=AZE_ECONOMIC_DIVERSIFICATION_TABLE,
    )


if __name__ == "__main__":
    main()
