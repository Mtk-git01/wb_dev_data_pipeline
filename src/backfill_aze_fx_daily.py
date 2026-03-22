from datetime import datetime
import re
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from google.cloud import bigquery

from src.config import PROJECT_ID, EXTERNAL_DATASET_ID, AZE_FX_DAILY_RAW_TABLE


def fetch_fx_for_date(dt: pd.Timestamp) -> pd.DataFrame:
    """
    Fetch CBAR FX XML for a specific date.
    Returns one-row-per-currency dataframe.
    If the XML does not exist for that day, returns empty dataframe.
    """
    date_str = dt.strftime("%d.%m.%Y")
    xml_url = f"https://cbar.az/currencies/{date_str}.xml"

    resp = requests.get(xml_url, timeout=30)
    if resp.status_code != 200:
        return pd.DataFrame()

    root = ET.fromstring(resp.content)

    as_of_date = pd.to_datetime(
        root.attrib.get("Date"),
        format="%d.%m.%Y",
        errors="coerce"
    ).date()

    rows = []
    for valute in root.findall(".//Valute"):
        code = valute.attrib.get("Code")
        if not code:
            continue

        nominal_text = valute.findtext("Nominal", default="1").strip()
        name = valute.findtext("Name", default=code).strip()
        value_text = valute.findtext("Value")

        if value_text is None:
            continue

        nominal_match = re.search(r"[\d.]+", nominal_text)
        nominal = float(nominal_match.group(0)) if nominal_match else 1.0

        rate_azn = float(value_text.replace(",", "."))
        rate_azn_per_unit = rate_azn / nominal if nominal else None

        rows.append({
            "as_of_date": as_of_date,
            "currency_name": name,
            "currency_code": code.upper().strip(),
            "nominal": nominal,
            "rate_azn": rate_azn,
            "rate_azn_per_unit": rate_azn_per_unit,
        })

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    keep_codes = ["USD", "EUR", "GBP", "RUB", "TRY", "KZT", "GEL", "CNY"]
    df = df[df["currency_code"].isin(keep_codes)].copy()
    return df.reset_index(drop=True)


def read_existing_fx_daily() -> pd.DataFrame:
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{EXTERNAL_DATASET_ID}.{AZE_FX_DAILY_RAW_TABLE}"

    query = f"SELECT * FROM `{table_ref}`"
    try:
        return client.query(query).to_dataframe()
    except Exception:
        return pd.DataFrame(
            columns=[
                "as_of_date",
                "currency_name",
                "currency_code",
                "nominal",
                "rate_azn",
                "rate_azn_per_unit",
            ]
        )


def overwrite_fx_daily(df: pd.DataFrame) -> None:
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{EXTERNAL_DATASET_ID}.{AZE_FX_DAILY_RAW_TABLE}"

    df = df.copy()
    df["as_of_date"] = pd.to_datetime(df["as_of_date"], errors="coerce").dt.date

    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=False,
        schema=[
            bigquery.SchemaField("as_of_date", "DATE"),
            bigquery.SchemaField("currency_name", "STRING"),
            bigquery.SchemaField("currency_code", "STRING"),
            bigquery.SchemaField("nominal", "FLOAT"),
            bigquery.SchemaField("rate_azn", "FLOAT"),
            bigquery.SchemaField("rate_azn_per_unit", "FLOAT"),
        ],
    )

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()


def backfill_fx_daily(start_date: str, end_date: str) -> pd.DataFrame:
    dates = pd.date_range(start=start_date, end=end_date, freq="D")

    collected = []
    for dt in dates:
        daily_df = fetch_fx_for_date(dt)
        if not daily_df.empty:
            collected.append(daily_df)

    if not collected:
        raise ValueError("No FX XML files were retrieved in the specified date range.")

    backfill_df = pd.concat(collected, ignore_index=True)

    existing_df = read_existing_fx_daily()
    combined = pd.concat([existing_df, backfill_df], ignore_index=True)

    combined["as_of_date"] = pd.to_datetime(combined["as_of_date"], errors="coerce").dt.date
    combined = (
        combined.sort_values(["as_of_date", "currency_code"])
        .drop_duplicates(subset=["as_of_date", "currency_code"], keep="last")
        .reset_index(drop=True)
    )

    overwrite_fx_daily(combined)
    return combined


if __name__ == "__main__":
    # example: backfill full 2024-01 to 2025-12
    end_date = pd.Timestamp.today().strftime("%Y-%m-%d")
    df = backfill_fx_daily(start_date="2024-01-01", end_date=end_date)
    print(f"Backfilled rows: {len(df)}")