import pandas as pd
from datetime import datetime, timezone

from src.config import TRADE_PARTNER_NAME, TRADE_SOURCE_NAME


def _series_or_na(df: pd.DataFrame, col: str):
    if col in df.columns:
        return df[col]
    return pd.Series([pd.NA] * len(df), index=df.index)


def transform_trade_long(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=[
            "reporter_name",
            "reporter_iso3",
            "year",
            "hs_code",
            "hs_label",
            "flow_code",
            "flow_name",
            "partner_code",
            "partner_name",
            "trade_value_usd",
            "net_weight_kg",
            "source_name",
            "load_timestamp",
        ])

    out = df.copy()

    requested_reporter_name = _series_or_na(out, "requested_reporter_name")
    reporter_desc = _series_or_na(out, "reporterDesc")
    out["reporter_name"] = requested_reporter_name.fillna(reporter_desc)

    requested_reporter_iso3 = _series_or_na(out, "requested_reporter_iso3")
    reporter_iso = _series_or_na(out, "reporterISO")
    out["reporter_iso3"] = requested_reporter_iso3.fillna(reporter_iso)

    out["year"] = pd.to_numeric(_series_or_na(out, "period"), errors="coerce").astype("Int64")

    requested_hs_code = _series_or_na(out, "requested_hs_code").astype("string")
    cmd_code = _series_or_na(out, "cmdCode").astype("string")
    out["hs_code"] = requested_hs_code.fillna(cmd_code)

    requested_hs_label = _series_or_na(out, "requested_hs_label")
    cmd_desc = _series_or_na(out, "cmdDesc")
    out["hs_label"] = requested_hs_label.fillna(cmd_desc)

    requested_flow_code = _series_or_na(out, "requested_flow_code").astype("string")
    flow_code = _series_or_na(out, "flowCode").astype("string")
    out["flow_code"] = requested_flow_code.fillna(flow_code)

    requested_flow_name = _series_or_na(out, "requested_flow_name")
    flow_desc = _series_or_na(out, "flowDesc")
    out["flow_name"] = requested_flow_name.fillna(flow_desc)

    partner_code = _series_or_na(out, "partnerCode").astype("string")
    out["partner_code"] = partner_code.fillna("0")

    partner_desc = _series_or_na(out, "partnerDesc")
    out["partner_name"] = partner_desc.fillna(TRADE_PARTNER_NAME)

    out["trade_value_usd"] = pd.to_numeric(_series_or_na(out, "primaryValue"), errors="coerce")
    out["net_weight_kg"] = pd.to_numeric(_series_or_na(out, "netWgt"), errors="coerce")

    out["source_name"] = TRADE_SOURCE_NAME
    out["load_timestamp"] = datetime.now(timezone.utc)

    out = out[
        [
            "reporter_name",
            "reporter_iso3",
            "year",
            "hs_code",
            "hs_label",
            "flow_code",
            "flow_name",
            "partner_code",
            "partner_name",
            "trade_value_usd",
            "net_weight_kg",
            "source_name",
            "load_timestamp",
        ]
    ].copy()

    out = out.dropna(subset=["reporter_iso3", "year", "hs_code", "flow_code"])

    out = (
        out.groupby(
            [
                "reporter_name",
                "reporter_iso3",
                "year",
                "hs_code",
                "hs_label",
                "flow_code",
                "flow_name",
                "partner_code",
                "partner_name",
                "source_name",
            ],
            as_index=False,
            dropna=False,
        )
        .agg(
            trade_value_usd=("trade_value_usd", "sum"),
            net_weight_kg=("net_weight_kg", "sum"),
        )
    )

    out["load_timestamp"] = datetime.now(timezone.utc)

    out = out.sort_values(
        ["reporter_iso3", "year", "hs_code", "flow_code"]
    ).reset_index(drop=True)

    return out


def latest_trade_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    work = df.dropna(subset=["trade_value_usd"]).copy()
    work = work.sort_values(["reporter_iso3", "hs_code", "flow_code", "year"])

    latest = (
        work.groupby(["reporter_iso3", "hs_code", "flow_code"], as_index=False)
        .tail(1)
        .reset_index(drop=True)
    )

    return latest