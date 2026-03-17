import pandas as pd


def list_available_countries(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["Country.Name", "Country.ISO"]
    return (
        df[cols]
        .dropna()
        .drop_duplicates()
        .sort_values(["Country.Name", "Country.ISO"])
        .reset_index(drop=True)
    )


def prepare_country_year_u5mr(df: pd.DataFrame, country_name_or_iso: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    required_cols = [
        "Country.Name",
        "Country.ISO",
        "Reference.Date",
        "Estimates",
        "Inclusion",
    ]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    work = df.copy()

    work = work[
        (work["Inclusion"] == 1)
        & (
            (work["Country.Name"] == country_name_or_iso)
            | (work["Country.ISO"] == country_name_or_iso)
        )
    ].copy()

    if work.empty:
        raise ValueError(f"No data found for: {country_name_or_iso}")

    work["Reference.Date"] = pd.to_numeric(work["Reference.Date"], errors="coerce")
    work["Estimates"] = pd.to_numeric(work["Estimates"], errors="coerce")

    if "Standard.Error.of.Estimates" in work.columns:
        work["Standard.Error.of.Estimates"] = pd.to_numeric(
            work["Standard.Error.of.Estimates"], errors="coerce"
        )

    work = work.dropna(subset=["Reference.Date", "Estimates"])
    work["Year"] = work["Reference.Date"].astype(float).astype(int)

    agg_dict = {"Estimates": "mean"}
    if "Standard.Error.of.Estimates" in work.columns:
        agg_dict["Standard.Error.of.Estimates"] = "mean"

    observed_yearly = (
        work.groupby("Year", as_index=True)
        .agg(agg_dict)
        .sort_index()
    )

    if observed_yearly.empty:
        raise ValueError(f"No usable yearly data found for: {country_name_or_iso}")

    all_years = pd.Index(
        range(int(observed_yearly.index.min()), int(observed_yearly.index.max()) + 1),
        name="Year"
    )

    interpolated_yearly = observed_yearly.reindex(all_years)
    interpolated_yearly["Estimates"] = interpolated_yearly["Estimates"].interpolate(method="linear")

    if "Standard.Error.of.Estimates" in interpolated_yearly.columns:
        interpolated_yearly["Standard.Error.of.Estimates"] = interpolated_yearly[
            "Standard.Error.of.Estimates"
        ].interpolate(method="linear")

    interpolated_yearly["is_interpolated"] = ~interpolated_yearly.index.isin(observed_yearly.index)

    return observed_yearly.reset_index(), interpolated_yearly.reset_index()


def prepare_all_countries_u5mr(df: pd.DataFrame) -> pd.DataFrame:
    countries = list_available_countries(df)
    all_results = []

    for _, row in countries.iterrows():
        country_name = row["Country.Name"]
        country_iso = row["Country.ISO"]

        try:
            _, interpolated_df = prepare_country_year_u5mr(df, country_iso)

            interpolated_df = interpolated_df.rename(
                columns={
                    "Year": "year",
                    "Estimates": "u5mr_estimate",
                    "Standard.Error.of.Estimates": "standard_error_of_estimates",
                }
            )

            interpolated_df["country_name"] = country_name
            interpolated_df["country_iso"] = country_iso

            keep_cols = [
                "country_name",
                "country_iso",
                "year",
                "u5mr_estimate",
                "standard_error_of_estimates",
                "is_interpolated",
            ]

            for col in keep_cols:
                if col not in interpolated_df.columns:
                    interpolated_df[col] = pd.NA

            all_results.append(interpolated_df[keep_cols])

        except Exception as e:
            print(f"Skipped {country_name} ({country_iso}): {e}")

    final_df = pd.concat(all_results, ignore_index=True)

    final_df["year"] = final_df["year"].astype("Int64")
    final_df["u5mr_estimate"] = pd.to_numeric(final_df["u5mr_estimate"], errors="coerce")
    final_df["standard_error_of_estimates"] = pd.to_numeric(
        final_df["standard_error_of_estimates"], errors="coerce"
    )

    return final_df