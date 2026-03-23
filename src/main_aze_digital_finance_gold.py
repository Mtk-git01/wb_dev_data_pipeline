
from pathlib import Path
import pandas as pd
from google.cloud import bigquery

from src.config import PROJECT_ID, EXTERNAL_DATASET_ID, AZE_SILVER_DATASET_ID, AZE_DIGITAL_FINANCE_TABLE, AZE_DIGITAL_FINANCE_SOURCE_NAME, AZE_NATIONAL_PAYMENT_SYSTEMS_PERIODIC_TABLE, AZE_PAYMENT_SERVICE_MONTHLY_TABLE, AZE_CARD_TRANSACTIONS_MONTHLY_TABLE, AZE_CUSTOMER_ACCOUNTS_EBANKING_MONTHLY_TABLE
from src.load_bigquery import upload_to_bigquery
from src.transform_aze_digital_finance_gold import build_aze_digital_finance_periodic


def read_table_from_bigquery(project_id: str, dataset_id: str, table_id: str) -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    return client.query(query).to_dataframe()


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    national_payment_systems_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_NATIONAL_PAYMENT_SYSTEMS_PERIODIC_TABLE)
    payment_service_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_PAYMENT_SERVICE_MONTHLY_TABLE)
    card_transactions_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_CARD_TRANSACTIONS_MONTHLY_TABLE)
    customer_accounts_ebanking_df = read_table_from_bigquery(PROJECT_ID, AZE_SILVER_DATASET_ID, AZE_CUSTOMER_ACCOUNTS_EBANKING_MONTHLY_TABLE)

    final_df = build_aze_digital_finance_periodic(
        national_payment_systems_df=national_payment_systems_df,
        payment_service_df=payment_service_df,
        card_transactions_df=card_transactions_df,
        customer_accounts_ebanking_df=customer_accounts_ebanking_df,
        source_name=AZE_DIGITAL_FINANCE_SOURCE_NAME,
    )

    final_df.to_csv(output_dir / "aze_digital_finance_periodic.csv", index=False)

    upload_to_bigquery(
        final_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=AZE_DIGITAL_FINANCE_TABLE,
    )


if __name__ == "__main__":
    main()
