from pathlib import Path
import pandas as pd
from google.cloud import bigquery
from google.api_core.exceptions import NotFound

from src.config import (
    PROJECT_ID,
    EXTERNAL_DATASET_ID,
    AZE_SILVER_DATASET_ID,
    AZE_BANK_OPS_TABLE_MONTHLY,
    AZE_BANK_OPS_SOURCE_NAME,
    AZE_MACRO_MONTHLY_TABLE,
    AZE_BANKING_MONTHLY_TABLE,
    AZE_POLICY_RATE_MONTHLY_TABLE,
    AZE_FX_DAILY_RAW_TABLE,
    AZE_FX_MONTHLY_TABLE,
)
from src.extract_aze_fx_rates import fetch_aze_fx_rates
from src.transform_aze_bank_ops import build_aze_fx_monthly_from_daily
from src.transform_aze_bank_ops_gold import build_aze_bank_ops_monthly
from src.load_bigquery import upload_to_bigquery


FX_DAILY_RAW_SCHEMA = [
    bigquery.SchemaField("as_of_date", "DATE"),
    bigquery.SchemaField("currency_name", "STRING"),
    bigquery.SchemaField("currency_code", "STRING"),
    bigquery.SchemaField("nominal", "FLOAT"),
    bigquery.SchemaField("rate_azn", "FLOAT"),
    bigquery.SchemaField("rate_azn_per_unit", "FLOAT"),
]

FX_MONTHLY_SCHEMA = [
    bigquery.SchemaField("month", "DATE"),
    bigquery.SchemaField("usd_azn", "FLOAT"),
    bigquery.SchemaField("eur_azn", "FLOAT"),
    bigquery.SchemaField("gbp_azn", "FLOAT"),
    bigquery.SchemaField("rub_azn", "FLOAT"),
    bigquery.SchemaField("try_azn", "FLOAT"),
    bigquery.SchemaField("kzt_azn", "FLOAT"),
    bigquery.SchemaField("gel_azn", "FLOAT"),
    bigquery.SchemaField("cny_azn", "FLOAT"),
]


def ensure_table_exists(
    project_id: str,
    dataset_id: str,
    table_id: str,
    schema: list[bigquery.SchemaField],
) -> None:
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    try:
        client.get_table(table_ref)
    except NotFound:
        table = bigquery.Table(table_ref, schema=schema)
        client.create_table(table)
        print(f"Created table: {table_ref}")


def append_fx_daily_to_bigquery_dedup(
    df: pd.DataFrame,
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> None:
    client = bigquery.Client(project=project_id)

    df = df.copy()
    df["as_of_date"] = pd.to_datetime(df["as_of_date"], errors="coerce").dt.date

    target_table = f"{project_id}.{dataset_id}.{table_id}"
    staging_table = f"{project_id}.{dataset_id}.{table_id}_staging"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,
    )
    load_job = client.load_table_from_dataframe(df, staging_table, job_config=job_config)
    load_job.result()

    merge_sql = f"""
    MERGE `{target_table}` AS T
    USING `{staging_table}` AS S
    ON T.as_of_date = S.as_of_date
       AND T.currency_code = S.currency_code
    WHEN NOT MATCHED THEN
      INSERT (
        as_of_date,
        currency_name,
        currency_code,
        nominal,
        rate_azn,
        rate_azn_per_unit
      )
      VALUES (
        S.as_of_date,
        S.currency_name,
        S.currency_code,
        S.nominal,
        S.rate_azn,
        S.rate_azn_per_unit
      )
    """
    merge_job = client.query(merge_sql)
    merge_job.result()

    client.delete_table(staging_table, not_found_ok=True)


def read_table_from_bigquery(project_id: str, dataset_id: str, table_id: str) -> pd.DataFrame:
    client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
    return client.query(query).to_dataframe()


def main() -> None:
    output_dir = Path("outputs/tables")
    output_dir.mkdir(parents=True, exist_ok=True)

    ensure_table_exists(
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=AZE_FX_DAILY_RAW_TABLE,
        schema=FX_DAILY_RAW_SCHEMA,
    )

    ensure_table_exists(
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=AZE_FX_MONTHLY_TABLE,
        schema=FX_MONTHLY_SCHEMA,
    )

    fx_daily_today = fetch_aze_fx_rates()
    fx_daily_today = fx_daily_today.drop_duplicates(subset=["as_of_date", "currency_code"]).reset_index(drop=True)

    append_fx_daily_to_bigquery_dedup(
        fx_daily_today,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=AZE_FX_DAILY_RAW_TABLE,
    )

    fx_daily_all = read_table_from_bigquery(
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=AZE_FX_DAILY_RAW_TABLE,
    )
    fx_monthly = build_aze_fx_monthly_from_daily(fx_daily_all)

    upload_to_bigquery(
        fx_monthly,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=AZE_FX_MONTHLY_TABLE,
    )

    macro_monthly = read_table_from_bigquery(
        project_id=PROJECT_ID,
        dataset_id=AZE_SILVER_DATASET_ID,
        table_id=AZE_MACRO_MONTHLY_TABLE,
    )
    banking_monthly = read_table_from_bigquery(
        project_id=PROJECT_ID,
        dataset_id=AZE_SILVER_DATASET_ID,
        table_id=AZE_BANKING_MONTHLY_TABLE,
    )
    policy_monthly = read_table_from_bigquery(
        project_id=PROJECT_ID,
        dataset_id=AZE_SILVER_DATASET_ID,
        table_id=AZE_POLICY_RATE_MONTHLY_TABLE,
    )

    final_df = build_aze_bank_ops_monthly(
        fx_monthly_df=fx_monthly,
        policy_monthly_df=policy_monthly,
        macro_monthly_df=macro_monthly,
        banking_monthly_df=banking_monthly,
        source_name=AZE_BANK_OPS_SOURCE_NAME,
    )

    final_df.to_csv(output_dir / "aze_bank_ops_monthly.csv", index=False)

    upload_to_bigquery(
        final_df,
        project_id=PROJECT_ID,
        dataset_id=EXTERNAL_DATASET_ID,
        table_id=AZE_BANK_OPS_TABLE_MONTHLY,
    )


if __name__ == "__main__":
    main()