import re
import requests
import pandas as pd
import xml.etree.ElementTree as ET


def fetch_aze_fx_rates() -> pd.DataFrame:
    page_url = "https://www.cbar.az/currency/rates?language=en"
    page = requests.get(page_url, timeout=30)
    page.raise_for_status()

    match = re.search(r"https://cbar\.az/currencies/\d{2}\.\d{2}\.\d{4}\.xml", page.text)
    if not match:
        raise ValueError("Could not find CBAR XML URL on exchange-rates page")

    xml_url = match.group(0)
    xml_resp = requests.get(xml_url, timeout=30)
    xml_resp.raise_for_status()

    root = ET.fromstring(xml_resp.content)

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
        raise ValueError("No FX rows parsed from CBAR XML")

    df = pd.DataFrame(rows)

    keep_codes = ["USD", "EUR", "GBP", "RUB", "TRY", "KZT", "GEL", "CNY"]
    df = df[df["currency_code"].isin(keep_codes)].copy()

    return df.reset_index(drop=True)