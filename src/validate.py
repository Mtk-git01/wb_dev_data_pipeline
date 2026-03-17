import pandas as pd


def validate_country_year_table(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """
    Returns:
        errors: pipeline should stop
        warnings: pipeline can continue, but should log
    """
    errors = []
    warnings = []

    required_cols = ["country_name", "country_iso", "year"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        errors.append(f"Missing required columns: {missing}")
        return errors, warnings

    # dup keys
    if "indicator_code" in df.columns:
        dup_keys = ["country_iso", "year", "indicator_code"]
    elif "u5mr_estimate" in df.columns:
        dup_keys = ["country_iso", "year"]
    else:
        dup_keys = ["country_iso", "year"]

    # null check
    country_iso_null_cnt = df["country_iso"].isna().sum()
    year_null_cnt = df["year"].isna().sum()

    if country_iso_null_cnt == len(df) and len(df) > 0:
        errors.append("country_iso is null for all rows.")
    elif country_iso_null_cnt > 0:
        warnings.append(f"country_iso contains {country_iso_null_cnt} null rows.")

    if year_null_cnt == len(df) and len(df) > 0:
        errors.append("year is null for all rows.")
    elif year_null_cnt > 0:
        warnings.append(f"year contains {year_null_cnt} null rows.")

    # value check
    if "value" in df.columns:
        value_null_cnt = df["value"].isna().sum()
        if value_null_cnt > 0:
            warnings.append(f"value contains {value_null_cnt} null rows.")

    if "u5mr_estimate" in df.columns:
        value_null_cnt = df["u5mr_estimate"].isna().sum()
        if value_null_cnt > 0:
            warnings.append(f"u5mr_estimate contains {value_null_cnt} null rows.")

    # Check Duplicate
    dup_cnt = df.duplicated(subset=dup_keys).sum()
    if dup_cnt > 0:
        warnings.append(f"Found {dup_cnt} duplicate rows by keys {dup_keys}.")

    # year range check
    if df["year"].notna().any():
        min_year = int(df["year"].dropna().min())
        max_year = int(df["year"].dropna().max())

        if min_year < 1900:
            warnings.append(f"Minimum year is unusually early: {min_year}")
        if max_year > 2100:
            warnings.append(f"Maximum year is unusually late: {max_year}")

    return errors, warnings


def print_validation_results(errors: list[str], warnings: list[str], table_name: str) -> None:
    if errors:
        print(f"[VALIDATION ERROR] {table_name}")
        for e in errors:
            print(f"  - {e}")

    if warnings:
        print(f"[VALIDATION WARNING] {table_name}")
        for w in warnings:
            print(f"  - {w}")

    if not errors and not warnings:
        print(f"[VALIDATION OK] {table_name}")