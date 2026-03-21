import pandas as pd
from pandas.api.types import is_numeric_dtype

from src.config import (
    GLOBAL_FINDEX_SOURCE_NAME,
    GLOBAL_FINDEX_RAW_TO_TARGET,
)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize raw column names:
    - lowercase
    - strip spaces
    - replace spaces and punctuation with underscores
    """
    out = df.copy()
    out.columns = (
        out.columns.str.strip()
        .str.lower()
        .str.replace(r"[^\w]+", "_", regex=True)
        .str.replace(r"_+", "_", regex=True)
        .str.strip("_")
    )
    return out


def _find_country_column(df: pd.DataFrame) -> str:
    candidates = [
        "country_name", "country", "economy", "economy_name", "countrynewwb"
    ]
    for col in candidates:
        if col in df.columns:
            return col
    raise ValueError("Could not find country name column in Global Findex raw file")


def _find_iso_column(df: pd.DataFrame) -> str:
    candidates = [
        "country_iso", "country_code", "iso3", "economy_code", "code", "codewb"
    ]
    for col in candidates:
        if col in df.columns:
            return col
    raise ValueError("Could not find ISO3 column in Global Findex raw file")


def _find_year_column(df: pd.DataFrame) -> str:
    candidates = ["year", "date"]
    for col in candidates:
        if col in df.columns:
            return col
    raise ValueError("Could not find year column in Global Findex raw file")


def _coerce_year(series: pd.Series) -> pd.Series:
    out = pd.to_numeric(series, errors="coerce").astype("Int64")
    return out


def _coerce_percent_columns(df: pd.DataFrame, metric_cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in metric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def transform_global_findex(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw Global Findex country-level data into a curated country-year table.

    Output columns:
    - country_name
    - country_iso
    - year
    - selected % indicators
    - source_name
    - load_timestamp
    """
    df = _normalize_columns(raw_df)

    country_col = _find_country_column(df)
    iso_col = _find_iso_column(df)
    year_col = _find_year_column(df)

    rename_map = {
        country_col: "country_name",
        iso_col: "country_iso",
        year_col: "year",
    }

    # keep only the curated subset if present
    for raw_col, target_col in GLOBAL_FINDEX_RAW_TO_TARGET.items():
        if raw_col in df.columns:
            rename_map[raw_col] = target_col

    df = df.rename(columns=rename_map)

    required_base_cols = ["country_name", "country_iso", "year"]
    missing_base = [c for c in required_base_cols if c not in df.columns]
    if missing_base:
        raise ValueError(f"Missing required base columns after rename: {missing_base}")

    metric_cols = [v for v in GLOBAL_FINDEX_RAW_TO_TARGET.values() if v in df.columns]

    keep_cols = required_base_cols + metric_cols
    df = df[keep_cols].copy()

    df["country_name"] = df["country_name"].astype(str).str.strip()
    df["country_iso"] = df["country_iso"].astype(str).str.upper().str.strip()
    df["year"] = _coerce_year(df["year"])

    df = _coerce_percent_columns(df, metric_cols)

    # remove aggregates if the raw file includes them and ISO is not 3 letters
    df = df[df["country_iso"].str.len() == 3].copy()

    # drop rows without identifiers
    df = df.dropna(subset=["country_name", "country_iso", "year"]).copy()

    # de-duplicate conservatively
    df = (
        df.sort_values(["country_iso", "year"])
          .drop_duplicates(subset=["country_iso", "year"], keep="first")
          .reset_index(drop=True)
    )

    df["source_name"] = GLOBAL_FINDEX_SOURCE_NAME
    df["load_timestamp"] = pd.Timestamp.utcnow()

    return df


def latest_non_null(country_year_df: pd.DataFrame) -> pd.DataFrame:
    """
    For each country, select the latest row with at least one non-null metric.
    """
    df = country_year_df.copy()

    metric_cols = [
        c for c in df.columns
        if c not in ["country_name", "country_iso", "year", "source_name", "load_timestamp"]
    ]

    if not metric_cols:
        raise ValueError("No metric columns found in Global Findex country-year table")

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