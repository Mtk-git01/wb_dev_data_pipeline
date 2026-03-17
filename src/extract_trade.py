import time
import pandas as pd
import comtradeapicall

from src.config import (
    TRADE_TARGETS,
    TRADE_START_YEAR,
    TRADE_END_YEAR,
    ISO3_TO_NUMERIC,
)


def fetch_trade_data_for_target(target: dict) -> pd.DataFrame:
    all_rows = []

    reporter_iso3 = target["reporter_iso3"]
    reporter_code = ISO3_TO_NUMERIC[reporter_iso3]
    hs_code = target["hs_code"]
    flow_code = target["flow_code"]

    for year in range(TRADE_START_YEAR, TRADE_END_YEAR + 1):
        df = comtradeapicall.previewFinalData(
            typeCode="C",
            freqCode="A",
            clCode="HS",
            period=str(year),
            reporterCode=reporter_code,
            cmdCode=hs_code,
            flowCode=flow_code,
            partnerCode="0",
            partner2Code=None,
            customsCode=None,
            motCode=None,
            maxRecords=500,
            format_output="JSON",
            aggregateBy=None,
            breakdownMode="classic",
            includeDesc=True,
        )

        if df is not None and not df.empty:
            df = df.copy()
            df["requested_reporter_iso3"] = reporter_iso3
            df["requested_reporter_name"] = target["reporter_name"]
            df["requested_hs_code"] = hs_code
            df["requested_hs_label"] = target["hs_label"]
            df["requested_flow_code"] = flow_code
            df["requested_flow_name"] = target["flow_name"]
            df["requested_year"] = year
            all_rows.append(df)

        time.sleep(0.2)

    valid_rows = [x for x in all_rows if x is not None and not x.empty]

    if not valid_rows:
        return pd.DataFrame()

    return pd.concat(valid_rows, ignore_index=True)


def fetch_all_trade_data() -> pd.DataFrame:
    all_frames = []

    for target in TRADE_TARGETS:
        df = fetch_trade_data_for_target(target)
        if df is not None and not df.empty:
            all_frames.append(df)

    valid_frames = [x for x in all_frames if x is not None and not x.empty]

    if not valid_frames:
        return pd.DataFrame()

    return pd.concat(valid_frames, ignore_index=True)