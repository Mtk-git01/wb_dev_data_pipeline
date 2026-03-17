from google.cloud import bigquery


def upload_u5mr_to_bigquery(df, project_id: str, dataset_id: str, table_id: str) -> None:
    client = bigquery.Client(project=project_id)

    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        schema=[
            bigquery.SchemaField("country_name", "STRING"),
            bigquery.SchemaField("country_iso", "STRING"),
            bigquery.SchemaField("year", "INTEGER"),
            bigquery.SchemaField("u5mr_estimate", "FLOAT"),
            bigquery.SchemaField("standard_error_of_estimates", "FLOAT"),
            bigquery.SchemaField("is_interpolated", "BOOL"),
        ],
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    print(f"Loaded {len(df):,} rows into {table_ref}")