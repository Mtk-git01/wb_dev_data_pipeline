from google.cloud import bigquery


def upload_to_bigquery(df, project_id: str, dataset_id: str, table_id: str) -> None:
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    schema_map = {
        # common WB-style indicator tables
        "country_name": "STRING",
        "country_iso": "STRING",
        "year": "INTEGER",
        "value": "FLOAT",
        "indicator_code": "STRING",
        "indicator_name": "STRING",
        "obs_status": "STRING",
        "decimal_places": "INTEGER",
        "source_name": "STRING",
        "load_timestamp": "TIMESTAMP",

        # U5MR
        "u5mr_estimate": "FLOAT",
        "standard_error_of_estimates": "FLOAT",
        "is_interpolated": "BOOL",

        # trade
        "reporter_name": "STRING",
        "reporter_iso3": "STRING",
        "hs_code": "STRING",
        "hs_label": "STRING",
        "flow_code": "STRING",
        "flow_name": "STRING",
        "partner_code": "STRING",
        "partner_name": "STRING",
        "trade_value_usd": "FLOAT",
        "net_weight_kg": "FLOAT",

        # city temperature
        "city_name": "STRING",
        "country_name": "STRING",
        "latitude": "FLOAT",
        "longitude": "FLOAT",
        "avg_temp_c_annual": "FLOAT",
        "observation_days": "INTEGER",
        
        # Bg
        "date": "DATE",
        "currency_code": "STRING",
        "local_price": "FLOAT",
        "dollar_price": "FLOAT",
        "usd_raw_index": "FLOAT",
        "usd_adjusted_index": "FLOAT",
        "gdp_dollar": "FLOAT",
    }

    schema = []
    for col in df.columns:
        if col in schema_map:
            schema.append(bigquery.SchemaField(col, schema_map[col]))

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        schema=schema,
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    print(f"Loaded {len(df):,} rows into {table_ref}")