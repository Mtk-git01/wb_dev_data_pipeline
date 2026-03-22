import re
from typing import List

import pandas as pd
import requests


def _parse_cpi_from_macro_page(url: str) -> pd.DataFrame:
    """
    Extract CPI yoy from SSC monthly macro page if a CPI / consumer price row is present.

    Output:
    - month
    - cpi_yoy
    - source_url

    Notes:
    SSC monthly macro pages are HTML pages, not a stable public API.
    This parser is a best-effort official-source scraper.
    """
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    # publication date on page
    pub_date_match = re.search(r"(\d{2}\.\d{2}\.\d{4})", resp.text)
    pub_date = pd.to_datetime(pub_date_match.group(1), dayfirst=True, errors="coerce") if pub_date_match else pd.NaT

    tables = pd.read_html(resp.text)
    if not tables:
        return pd.DataFrame()

    best = None
    for t in tables:
        lower = " ".join(map(str, t.columns)).lower() + " " + " ".join(map(str, t.iloc[:, 0].astype(str).tolist())).lower()
        if "consumer" in lower or "price" in lower or "inflation" in lower:
            best = t.copy()
            break

    if best is None:
        return pd.DataFrame()

    # try to locate row mentioning CPI / consumer price
    first_col = best.iloc[:, 0].astype(str)
    mask = first_col.str.lower().str.contains("consumer|price|inflation", na=False)
    if not mask.any():
        return pd.DataFrame()

    row = best.loc[mask].iloc[0]
    # choose first numeric-looking value after label
    cpi_val = None
    for val in row.iloc[1:].tolist():
        s = str(val).replace(",", ".").strip()
        try:
            cpi_val = float(s)
            break
        except Exception:
            continue

    if cpi_val is None or pd.isna(pub_date):
        return pd.DataFrame()

    out = pd.DataFrame({
        "month": [pub_date.to_period("M").to_timestamp()],
        "cpi_yoy": [cpi_val],
        "source_url": [url],
    })
    return out


def fetch_aze_cpi_range(max_pages: int = 24) -> pd.DataFrame:
    """
    Scrape recent SSC monthly macro pages and collect CPI yoy when present.
    """
    urls = ["https://www.stat.gov.az/news/macroeconomy.php?lang=en&page=1"] + [
        f"https://www.stat.gov.az/news/macroeconomy.php?arxiv=1&lang=en&page={p}"
        for p in range(1, max_pages + 1)
    ]

    frames: List[pd.DataFrame] = []
    for url in urls:
        try:
            df = _parse_cpi_from_macro_page(url)
            if not df.empty:
                frames.append(df)
        except Exception:
            continue

    if not frames:
        raise ValueError("No SSC CPI-like data parsed from macro pages")

    out = pd.concat(frames, ignore_index=True)
    out = (
        out.sort_values("month")
           .drop_duplicates(subset=["month"], keep="last")
           .reset_index(drop=True)
    )
    return out