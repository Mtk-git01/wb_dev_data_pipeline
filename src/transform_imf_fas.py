import pandas as pd

from src.config import IMF_FAS_SOURCE_NAME, IMF_FAS_SERIES_TO_TARGET


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


def _extract_country_iso_from_series_code(series_code: str) -> str | None:
    """
    IMF FAS series code example:
      BEL.FA21_COMBANK.NUM.A
      COD.COMBANK.NUM.A

    We take the first token before the first dot as ISO3 if length == 3.
    """
    if pd.isna(series_code):
        return None

    token = str(series_code).split(".")[0].strip().upper()
    if len(token) == 3:
        return token
    return None


def _extract_series_key_from_series_code(series_code: str) -> str | None:
    """
    IMF FAS series examples:
      BEL.FA21_COMBANK.NUM.A
      COD.COMBANK.NUM.A
      PNG.FA63.NUM.A
    """
    if pd.isna(series_code):
        return None

    code = str(series_code).strip().upper()
    parts = code.split(".")

    if len(parts) < 2:
        return None

    body = ".".join(parts[1:])  # drop ISO3

    if body.startswith("FA21_COMBANK."):
        return "FA21_COMBANK"
    if body.startswith("COMBANK."):
        return "COMBANK"
    if body.startswith("FA63."):
        return "FA63"

    return None


def transform_imf_fas(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform IMF FAS bulk export (wide format: one row per country-series,
    year columns as 2004...2025) into a curated country-year table.

    Expected important raw columns:
      - COUNTRY
      - SERIES_CODE
      - INDICATOR
      - 2004 ... 2025
    """
    df = _normalize_columns(raw_df)

    required_cols = ["country", "series_code"]
    missing_required = [c for c in required_cols if c not in df.columns]
    if missing_required:
        raise ValueError(f"Missing required IMF FAS columns: {missing_required}")

    year_cols = [c for c in df.columns if c.isdigit()]
    if not year_cols:
        raise ValueError("No year columns found in IMF FAS raw file")

    df["country_name"] = df["country"].astype(str).str.strip()
    df["country_iso"] = df["series_code"].apply(_extract_country_iso_from_series_code)
    df["series_key"] = df["series_code"].apply(_extract_series_key_from_series_code)
    print(df["series_code"].head(20).tolist())
    print(df["series_key"].head(20).tolist())
    print(df["series_key"].value_counts(dropna=False))

    # keep only curated series
    df = df[df["series_key"].isin(IMF_FAS_SERIES_TO_TARGET.keys())].copy()

    if df.empty:
        raise ValueError(
            "No matching IMF FAS series found. "
            "Check IMF_FAS_SERIES_TO_TARGET against your SERIES_CODE values."
        )

    long_df = df.melt(
        id_vars=["country_name", "country_iso", "series_key"],
        value_vars=year_cols,
        var_name="year",
        value_name="value",
    )

    long_df["year"] = pd.to_numeric(long_df["year"], errors="coerce").astype("Int64")
    long_df["value"] = pd.to_numeric(long_df["value"], errors="coerce")
    long_df["target_col"] = long_df["series_key"].map(IMF_FAS_SERIES_TO_TARGET)

    wide_df = long_df.pivot_table(
        index=["country_name", "country_iso", "year"],
        columns="target_col",
        values="value",
        aggfunc="first",
    ).reset_index()

    wide_df["country_name"] = wide_df["country_name"].astype(str).str.strip()
    wide_df["country_iso"] = wide_df["country_iso"].astype(str).str.upper().str.strip()

    wide_df = wide_df[wide_df["country_iso"].str.len() == 3].copy()
    wide_df = wide_df.dropna(subset=["country_name", "country_iso", "year"]).copy()

    wide_df = (
        wide_df.sort_values(["country_iso", "year"])
        .drop_duplicates(subset=["country_iso", "year"], keep="first")
        .reset_index(drop=True)
    )

    wide_df["source_name"] = IMF_FAS_SOURCE_NAME
    wide_df["load_timestamp"] = pd.Timestamp.utcnow()

    return wide_df


def latest_non_null(country_year_df: pd.DataFrame) -> pd.DataFrame:
    df = country_year_df.copy()

    metric_cols = [
        c for c in df.columns
        if c not in ["country_name", "country_iso", "year", "source_name", "load_timestamp"]
    ]

    if not metric_cols:
        raise ValueError("No metric columns found in IMF FAS country-year table")

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