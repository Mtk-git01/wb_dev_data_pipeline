from __future__ import annotations

from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup


def _fetch_html(url: str) -> str:
    """
    Fetch HTML text from a URL.
    """
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.text


def _parse_cbar_table_rows(
    html_text: str,
    page_type: str,
) -> pd.DataFrame:
    """
    Parse CBAR infoblock pages that use the following structure:

    <div class="table_items table-pagination">
        <div class="table_row">
            <div class="valuta">29.12.2024</div>
            <div class="kod">10959.5</div>
        </div>
        ...
    </div>

    page_type:
    - "reserves" -> numeric value
    - "policy_rate" -> percent value like "7.25%"

    Returns columns:
    - as_of_date
    - value
    """
    soup = BeautifulSoup(html_text, "html.parser")
    rows = soup.select("div.table_row")

    parsed = []
    for row in rows:
        date_node = row.select_one("div.valuta")
        value_node = row.select_one("div.kod")

        if not date_node or not value_node:
            continue

        date_text = date_node.get_text(strip=True)
        value_text = value_node.get_text(strip=True)

        as_of_date = pd.to_datetime(date_text, format="%d.%m.%Y", errors="coerce")
        if pd.isna(as_of_date):
            continue

        if page_type == "policy_rate":
            value_text = value_text.replace("%", "").strip()

        value = pd.to_numeric(value_text, errors="coerce")
        if pd.isna(value):
            continue

        parsed.append(
            {
                "as_of_date": as_of_date,
                "value": float(value),
            }
        )

    return pd.DataFrame(parsed)


def fetch_aze_fx_reserves_year(year: int) -> pd.DataFrame:
    """
    Fetch monthly official FX reserves from CBAR year page.

    Output columns:
    - month
    - official_fx_reserves_usd_mn
    - source_url
    """
    url = f"https://www.cbar.az/infoblocks/money_reserve_usd?language=en&year={year}"
    html_text = _fetch_html(url)

    if "Official foreign exchange reserves" not in html_text:
        raise ValueError(f"Unexpected reserves page structure for year={year}")

    df = _parse_cbar_table_rows(html_text=html_text, page_type="reserves")
    if df.empty:
        raise ValueError(f"No reserves rows parsed from CBAR page for year={year}")

    df["month"] = df["as_of_date"].dt.to_period("M").dt.to_timestamp()
    df["official_fx_reserves_usd_mn"] = df["value"]
    df["source_url"] = url

    # One record per month; keep latest observation in that month
    df = (
        df.sort_values("as_of_date")
        .drop_duplicates(subset=["month"], keep="last")
        .reset_index(drop=True)
    )

    return df[["month", "official_fx_reserves_usd_mn", "source_url"]]


def fetch_aze_fx_reserves_range(start_year: int, end_year: int) -> pd.DataFrame:
    """
    Fetch monthly official FX reserves across a year range.

    Output columns:
    - month
    - official_fx_reserves_usd_mn
    - source_url
    """
    frames: List[pd.DataFrame] = []

    for year in range(start_year, end_year + 1):
        try:
            yearly_df = fetch_aze_fx_reserves_year(year)
            if not yearly_df.empty:
                frames.append(yearly_df)
        except Exception as e:
            print(f"[WARN] reserves year {year} skipped: {e}")

    if not frames:
        raise ValueError("No CBAR reserves data retrieved")

    df = pd.concat(frames, ignore_index=True)
    df = (
        df.sort_values("month")
        .drop_duplicates(subset=["month"], keep="last")
        .reset_index(drop=True)
    )
    return df


def fetch_aze_policy_rate_year(year: int) -> pd.DataFrame:
    """
    Fetch refinancing-rate events from CBAR year page.

    Output columns:
    - effective_date
    - refinancing_rate
    - corridor_floor
    - corridor_ceiling
    - source_url

    Note:
    The provided CBAR source clearly exposes refinancing rate values by date.
    Corridor floor / ceiling are not exposed in the same simple infoblock table,
    so they are left as null here unless supplemented from another source later.
    """
    url = f"https://www.cbar.az/infoblocks/corridor_percent?language=en&year={year}"
    html_text = _fetch_html(url)

    if "Refinancing rate" not in html_text:
        raise ValueError(f"Unexpected refinancing-rate page structure for year={year}")

    df = _parse_cbar_table_rows(html_text=html_text, page_type="policy_rate")
    if df.empty:
        raise ValueError(f"No policy-rate rows parsed from CBAR page for year={year}")

    df = df.rename(
        columns={
            "as_of_date": "effective_date",
            "value": "refinancing_rate",
        }
    )
    df["source_url"] = url
    df["corridor_floor"] = pd.NA
    df["corridor_ceiling"] = pd.NA

    df = (
        df.sort_values("effective_date")
        .drop_duplicates(subset=["effective_date"], keep="last")
        .reset_index(drop=True)
    )

    return df[
        [
            "effective_date",
            "refinancing_rate",
            "corridor_floor",
            "corridor_ceiling",
            "source_url",
        ]
    ]


def fetch_aze_policy_rate_range(start_year: int, end_year: int) -> pd.DataFrame:
    """
    Fetch refinancing-rate events across a year range.

    Output columns:
    - effective_date
    - refinancing_rate
    - corridor_floor
    - corridor_ceiling
    - source_url
    """
    frames: List[pd.DataFrame] = []

    for year in range(start_year, end_year + 1):
        try:
            yearly_df = fetch_aze_policy_rate_year(year)
            if not yearly_df.empty:
                frames.append(yearly_df)
        except Exception as e:
            print(f"[WARN] policy rate year {year} skipped: {e}")

    if not frames:
        raise ValueError("No CBAR refinancing-rate data retrieved")

    df = pd.concat(frames, ignore_index=True)
    df = (
        df.sort_values("effective_date")
        .drop_duplicates(subset=["effective_date"], keep="last")
        .reset_index(drop=True)
    )
    return df