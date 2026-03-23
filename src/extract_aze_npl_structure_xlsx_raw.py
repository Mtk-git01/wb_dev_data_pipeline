
from __future__ import annotations

from pathlib import Path
from typing import List

import openpyxl
import pandas as pd

from src.config import AZE_BANKING_BULLETIN_XLSX_RAW_DIR
from src.extract_aze_bulletin_common import add_country_fields, dedup_keep_latest, find_sheet, iter_xlsx_files, normalize_text, parse_bulletin_period_from_filename, to_num


def parse_aze_npl_structure_xlsx_file(xlsx_path: Path) -> pd.DataFrame:
    bulletin_period = parse_bulletin_period_from_filename(xlsx_path.name)
    wb = openpyxl.load_workbook(xlsx_path, data_only=True, read_only=True)
    ws = find_sheet(wb, "5.6")

    date_cols = {}
    for c in range(2, ws.max_column + 1):
        v = ws.cell(6, c).value
        ts = pd.to_datetime(v, errors="coerce")
        if pd.notna(ts):
            date_cols[c] = pd.Timestamp(ts).replace(day=1)

    rows = []
    for c, period_date in date_cols.items():
        rec = {
            "period_date": period_date,
            "period_type": "monthly",
            "source_file": xlsx_path.name,
            "bulletin_period": bulletin_period,
        }
        for r in range(7, 25):
            label = normalize_text(ws.cell(r, 1).value)
            value = to_num(ws.cell(r, c).value)
            if value is None:
                continue
            if "qeyri-işlək kredit (qi̇k)" in label or "qeyri-işlək kredit (qik)" in label:
                rec["npl_total_mn_azn"] = value
            elif "biznes kreditləri" in label and "qik" not in label:
                rec["npl_business_mn_azn"] = value
            elif "istehlak kreditləri" in label and "qik" not in label:
                rec["npl_consumer_mn_azn"] = value
            elif "ipoteka kreditləri" in label and "qik" not in label:
                rec["npl_mortgage_mn_azn"] = value
            elif "qik/kredit portfeli" in label:
                rec["npl_ratio_pct"] = value * 100 if value <= 1 else value
            elif "biznes (qik)/biznes kreditləri" in label:
                rec["npl_business_ratio_pct"] = value * 100 if value <= 1 else value
            elif "istehlak (qik)/istehlak kreditləri" in label:
                rec["npl_consumer_ratio_pct"] = value * 100 if value <= 1 else value
            elif "ipoteka (qik)/ipoteka kreditləri" in label:
                rec["npl_mortgage_ratio_pct"] = value * 100 if value <= 1 else value
        rows.append(rec)

    if not rows:
        raise ValueError(f"No rows parsed from sheet 5.6 in {xlsx_path.name}")
    return add_country_fields(pd.DataFrame(rows))


def load_aze_npl_structure_xlsx_raw() -> pd.DataFrame:
    frames: List[pd.DataFrame] = [parse_aze_npl_structure_xlsx_file(p) for p in iter_xlsx_files(AZE_BANKING_BULLETIN_XLSX_RAW_DIR)]
    return dedup_keep_latest(pd.concat(frames, ignore_index=True), ["country_iso", "period_date", "period_type"])
