import pandas as pd

from src.config import WGI_SOURCE_NAME


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = (
        out.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w]+", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )
    return out


def transform_wgi(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = _normalize_columns(raw_df)

    # 実ファイルに合わせた列名
    required_cols = [
        "economy_name",
        "economy_code",
        "year",
        "governance_dimension",
        "governance_estimate_approx_2_5_to_2_5",
    ]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required WGI columns: {missing}")

    df = df.rename(columns={
        "economy_name": "country_name",
        "economy_code": "country_iso",
        "governance_dimension": "dimension_code",
        "governance_estimate_approx_2_5_to_2_5": "estimate_value",
    })

    df["country_name"] = df["country_name"].astype(str).str.strip()
    df["country_iso"] = df["country_iso"].astype(str).str.upper().str.strip()
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["dimension_code"] = df["dimension_code"].astype(str).str.strip().str.lower()
    df["estimate_value"] = pd.to_numeric(df["estimate_value"], errors="coerce")

    # WGIのdimension codeをターゲット列名に変換
    dimension_map = {
        "va": "voice_accountability",
        "pv": "political_stability",
        "ge": "government_effectiveness",
        "rq": "regulatory_quality",
        "rl": "rule_of_law",
        "cc": "control_of_corruption",
    }

    df = df[df["dimension_code"].isin(dimension_map.keys())].copy()
    if df.empty:
        raise ValueError("No matching WGI governance dimensions found")

    df["target_col"] = df["dimension_code"].map(dimension_map)

    wide_df = df.pivot_table(
        index=["country_name", "country_iso", "year"],
        columns="target_col",
        values="estimate_value",
        aggfunc="first",
    ).reset_index()

    wide_df = wide_df[wide_df["country_iso"].str.len() == 3].copy()
    wide_df = wide_df.dropna(subset=["country_name", "country_iso", "year"]).copy()

    wide_df = (
        wide_df.sort_values(["country_iso", "year"])
        .drop_duplicates(subset=["country_iso", "year"], keep="first")
        .reset_index(drop=True)
    )

    wide_df["source_name"] = WGI_SOURCE_NAME
    wide_df["load_timestamp"] = pd.Timestamp.utcnow()

    return wide_df


def latest_non_null(country_year_df: pd.DataFrame) -> pd.DataFrame:
    df = country_year_df.copy()

    metric_cols = [
        c for c in df.columns
        if c not in ["country_name", "country_iso", "year", "source_name", "load_timestamp"]
    ]

    if not metric_cols:
        raise ValueError("No metric columns found in WGI country-year table")

    df["_non_null_metric_count"] = df[metric_cols].notna().sum(axis=1)
    df = df[df["_non_null_metric_count"] > 0].copy()

    latest = (
        df.sort_values(["country_iso", "year"])
        .groupby("country_iso", as_index=False)
        .tail(1)
        .drop(columns=["_non_null_metric_count"])
        .reset_index(drop=True)
    )

    return latest