# # World Bank Development Statistics Pipeline and Azerbaijan CPF Analysis

Reproducible ETL pipelines for World Bank development indicators, logistics, governance and financial access datasets, with analysis-ready outputs and Azerbaijan CPF-focused analytical use cases.

## Overview
This repository builds development-data pipelines that:

- extract public international data from source-oriented datasets and APIs
- transform raw or raw-data-near inputs into curated analytical tables
- validate structural and data-quality conditions
- load outputs into BigQuery
- support downstream cross-country and city-level analysis

Current implemented pipelines include:

### World Bank API-based indicators
- Girls’ primary completion rate
- GDP per capita
- Net ODA received per capita
- Learning-adjusted years of schooling (LAYS)

### World Bank source-oriented non-API datasets
- Worldwide Governance Indicators (WGI)

### External source-oriented datasets
- Under-five mortality (U5MR) from UN-IGME
- Global Findex from the World Bank
- Financial Access Survey (FAS) from IMF
- Merchandise trade flows from UN Comtrade
- City temperature time series from Open-Meteo
- Big Mac Index from The Economist

---

## Why this repository
This project is designed to demonstrate:

- source-oriented data extraction
- reproducible ETL design
- explicit data-lineage awareness
- country-year and city-year data modeling
- validation before loading
- cloud-ready analytical storage in BigQuery
- the ability to transform source statistical inputs into curated analytical assets

A central design principle is to distinguish between:
- **official or World Bank-managed development indicators**
- **external public datasets used as complementary analytical inputs**

To reflect this, BigQuery tables are organized into two datasets:

- `wb_dev_stats`  
  for World Bank API-derived tables and World Bank source datasets such as WGI

- `external_dev_stats`  
  for external datasets such as UN-IGME, Global Findex, IMF FAS, UN Comtrade, Open-Meteo, and Big Mac Index

---

## BigQuery datasets

### 1) World Bank / World Bank-managed dataset
Dataset:
- `worldbank01.wb_dev_stats`

This dataset contains indicators retrieved directly from the World Bank API and other World Bank-managed data products.

### 2) External source-oriented dataset
Dataset:
- `worldbank01.external_dev_stats`

This dataset contains analytical tables derived from external public sources.

---

## Current pipelines

## 1) U5MR pipeline
The U5MR workflow uses the **UN-IGME observational database** as the upstream source, rather than relying only on downstream redistribution through World Bank Open Data.

This reflects an explicit **data lineage** choice:
- use the original source-side dataset
- treat it as the **source-of-truth raw input**
- transform it into an analysis-ready annual country-year table

### U5MR transformations
- filter to included observations
- convert irregular observation dates into annual records
- aggregate multiple observations within the same year
- standardize to **one row per country per year**
- fill missing internal years using **linear interpolation**
- flag interpolated years using `is_interpolated`

### Linear interpolation
### Note on missing data
The WDI documentation notes that development data may contain missing values and may not always be fully comparable across countries and years, and that multiple aggregation methods are used depending on the indicator. In this project, I use a simple **linear interpolation** method for demonstration purposes rather than attempting to reproduce the official aggregation rules.

If a value is observed at year `x0` and another value is observed at year `x1`, then the interpolated value at year `x` is:

`y(x) = y0 + ((x - x0) / (x1 - x0)) * (y1 - y0)`

where:

- `x0`: earlier observed year
- `x1`: later observed year
- `y0`: observed value at `x0`
- `y1`: observed value at `x1`

This converts irregularly spaced observations into a continuous annual analytical series.

### Important note
The U5MR table in this repository is **not the official UN-IGME modelled estimate series**.  
It is an **annualized and interpolated analytical table** derived from the underlying observational source data.

### BigQuery table
Dataset:
- `external_dev_stats`

Table:
- `worldbank01.external_dev_stats.u5mr_country_year`

### Main columns
- `country_name`
- `country_iso`
- `year`
- `u5mr_estimate`
- `standard_error_of_estimates`
- `is_interpolated`

---

## 2) Girls’ primary completion pipeline
This workflow retrieves:

- **Primary completion rate, female (% of relevant age group)**
- Indicator code: `SE.PRM.CMPT.FE.ZS`

### Source
- World Bank API

### Outputs
Two tables are created:

#### Country-year table
- full country-year time series
- useful for trend analysis and panel joins

#### Latest country snapshot
- most recent non-null value for each country
- useful for cross-country comparison and ranking

### BigQuery tables
Dataset:
- `wb_dev_stats`

Tables:
- `worldbank01.wb_dev_stats.girls_primary_completion_country_year`
- `worldbank01.wb_dev_stats.girls_primary_completion_country_latest`

---

## 3) GDP per capita pipeline
This workflow retrieves:

- **GDP per capita (current US$)**
- Indicator code: `NY.GDP.PCAP.CD`

### Source
- World Bank API

### Outputs
Two tables are created:

#### Country-year table
- full country-year time series
- useful for panel analysis and joins with education, health, aid, trade, governance, and financial access indicators

#### Latest country snapshot
- most recent non-null value for each country
- useful for cross-country comparison

### BigQuery tables
Dataset:
- `wb_dev_stats`

Tables:
- `worldbank01.wb_dev_stats.gdp_per_capita_country_year`
- `worldbank01.wb_dev_stats.gdp_per_capita_country_latest`

---

## 4) Net ODA received per capita pipeline
This workflow retrieves:

- **Net ODA received per capita (current US$)**
- Indicator code: `DT.ODA.ODAT.PC.ZS`

### Source
- World Bank API

### Outputs
Two tables are created:

#### Country-year table
- full country-year time series
- useful for aid and development trajectory analysis

#### Latest country snapshot
- most recent non-null value for each country

### BigQuery tables
Dataset:
- `wb_dev_stats`

Tables:
- `worldbank01.wb_dev_stats.oda_received_per_capita_country_year`
- `worldbank01.wb_dev_stats.oda_received_per_capita_country_latest`

---

## 5) LAYS pipeline
This workflow retrieves:

- **Learning-adjusted years of schooling**
- Indicator code: `HD.HCI.LAYS`

### Source
- World Bank API

### Why this indicator matters
LAYS is designed to go beyond years of schooling alone by incorporating learning quality into a schooling-based measure.  
This makes it especially useful when comparing educational attainment in a more development-relevant way.

### Outputs
Two tables are created:

#### Country-year table
- full country-year time series

#### Latest country snapshot
- most recent non-null value for each country

### BigQuery tables
Dataset:
- `wb_dev_stats`

Tables:
- `worldbank01.wb_dev_stats.lays_country_year`
- `worldbank01.wb_dev_stats.lays_country_latest`

---

## 6) WGI pipeline
This workflow uses the **Worldwide Governance Indicators (WGI)** as a World Bank-managed governance dataset covering six core dimensions of institutional quality.

### Source
- World Bank Worldwide Governance Indicators (WGI)

### Why this matters analytically
WGI provides a governance layer that can be joined with development, education, health, trade, and financial access indicators.  
This makes it possible to study relationships between:
- governance quality and human development
- institutional quality and economic performance
- governance and financial access
- governance and trade structure

### Current governance dimensions included
- Voice and Accountability
- Political Stability and Absence of Violence/Terrorism
- Government Effectiveness
- Regulatory Quality
- Rule of Law
- Control of Corruption

### Transformations
The current WGI input file is structured as:
- one row per economy × governance dimension × year

The workflow:
- reads the official WGI Excel bulk file
- standardizes identifiers
- maps governance dimension codes
- pivots dimension rows into a single country-year analytical table
- loads curated outputs into BigQuery

### Outputs
Two tables are created:

#### Country-year table
- full country-year time series
- useful for panel analysis and joins with GDP, U5MR, trade, and financial access indicators

#### Latest country snapshot
- most recent non-null value for each country
- useful for cross-country institutional comparison

### BigQuery tables
Dataset:
- `wb_dev_stats`

Tables:
- `worldbank01.wb_dev_stats.wgi_country_year`
- `worldbank01.wb_dev_stats.wgi_country_latest`

### Main columns
- `country_name`
- `country_iso`
- `year`
- `voice_accountability`
- `political_stability`
- `government_effectiveness`
- `regulatory_quality`
- `rule_of_law`
- `control_of_corruption`
- `source_name`
- `load_timestamp`

---

## 7) Global Findex pipeline
This workflow uses the **World Bank Global Findex** country-level dataset as a complementary source for financial inclusion analysis.

### Source
- World Bank Global Findex

### Why this matters analytically
Global Findex provides demand-side indicators on account ownership, financial access, digital payments, mobile money, and related financial inclusion outcomes.  
In this repository it is treated as a complementary dataset that can be joined with:
- GDP per capita
- U5MR
- girls’ primary completion
- LAYS
- WGI
- trade indicators

This makes it possible to study relationships between:
- financial inclusion and development outcomes
- digital payments and income level
- account ownership and gender-relevant development patterns
- governance and financial access

### Important note on missing values
Indicator coverage varies across countries and survey waves.  
Nulls are retained as source-faithful missing values rather than being imputed.

### Outputs
Two tables are created:

#### Country-year table
- historical country-year data
- useful for panel analysis and joins with macro and development indicators

#### Latest country snapshot
- most recent non-null record for each country
- useful for cross-country comparison

### BigQuery tables
Dataset:
- `external_dev_stats`

Tables:
- `worldbank01.external_dev_stats.global_findex_country_year`
- `worldbank01.external_dev_stats.global_findex_country_latest`

### Main columns
- `country_name`
- `country_iso`
- `year`
- `account_ownership_pct`
- `financial_institution_account_pct`
- `mobile_money_account_pct`
- `digital_payment_pct`
- `borrowed_from_financial_institution_pct`
- `source_name`
- `load_timestamp`

---

## 8) IMF FAS pipeline
This workflow uses the **IMF Financial Access Survey (FAS)** as a complementary source for supply-side and institutional financial access statistics.

### Source
- IMF Financial Access Survey (FAS)

### Why this matters analytically
IMF FAS provides country-reported annual financial access and usage statistics, which complement the demand-side perspective of Global Findex.  
This makes it possible to compare:
- financial sector structure and financial inclusion
- commercial banking depth and development outcomes
- mobile money activity and country trajectories
- governance, financial institutions, and access patterns

### Current curated subset
The current implementation keeps a small curated subset of annual series from the FAS bulk file, including:
- number of commercial banks
- borrowers from commercial banks
- active mobile money accounts

This subset is intentionally narrow for a stable first analytical layer and can be extended later.

### Transformations
The current FAS input file is structured as:
- one row per country × series
- annual values stored in year columns

The workflow:
- reads the IMF FAS bulk CSV
- extracts ISO3 from `SERIES_CODE`
- maps selected FAS series into curated analytical variables
- melts year columns into a long structure
- pivots into a one-row-per-country-per-year analytical table
- loads curated outputs into BigQuery

### Outputs
Two tables are created:

#### Country-year table
- historical country-year data
- useful for joins with GDP, governance, education, and financial inclusion indicators

#### Latest country snapshot
- most recent non-null record for each country
- useful for cross-country comparison

### BigQuery tables
Dataset:
- `external_dev_stats`

Tables:
- `worldbank01.external_dev_stats.imf_fas_country_year`
- `worldbank01.external_dev_stats.imf_fas_country_latest`

### Main columns
- `country_name`
- `country_iso`
- `year`
- `commercial_banks_number`
- `borrowers_commercial_banks_number`
- `active_mobile_money_accounts_number`
- `source_name`
- `load_timestamp`

---

## 9) Trade pipeline
This repository also includes a trade-data workflow built from **UN Comtrade**, chosen as a more source-oriented and raw-data-near input for international merchandise trade analysis.

This reflects a deliberate **data lineage** choice:
- instead of relying only on downstream summary tables
- the workflow retrieves trade records from UN Comtrade
- and transforms them into analysis-ready country-year trade tables

### Why UN Comtrade
UN Comtrade is treated here as a **primary-data-near trade source** for internationally reported merchandise trade flows.

Using this source makes it possible to work closer to the original reporting structure of trade statistics before transforming them into curated analytical tables.

### Current trade scope
The current implementation focuses on a small, interpretable set of country-product-flow combinations chosen to support development-oriented analysis.

#### Luxury goods / high-end consumption proxy
- Jewellery imports
  - Japan
  - Kazakhstan

#### Developing-country-origin commodity exports
- Coffee exports
  - Brazil
  - Ghana
- Cocoa exports
  - Brazil
  - Ghana

This design allows the trade module to capture both:
- **high-value consumption-oriented trade**
- **commodity exports linked to developing-country production structures**

### Trade transformations
The trade workflow:
- retrieves annual trade data from UN Comtrade
- keeps the extraction layer relatively close to the raw source structure
- selects essential reporting fields for analytical use
- standardizes outputs into country-year records
- loads curated outputs into BigQuery

The curated trade tables use:
- `primaryValue` from source data as `trade_value_usd`
- `netWgt` from source data as `net_weight_kg`

### Why this matters analytically
This trade pipeline is designed not as a standalone trade exercise, but as a module that can be joined with other development indicators in the repository, such as:

- U5MR
- girls’ primary completion
- GDP per capita
- Net ODA received per capita
- LAYS
- WGI
- Global Findex
- IMF FAS

This makes it possible to study relationships between:
- export structure and human development
- commodity dependence and social indicators
- high-end import exposure and economic development level
- trade patterns and broader country trajectories

### BigQuery tables
Dataset:
- `external_dev_stats`

Tables:
- `worldbank01.external_dev_stats.trade_country_year_long`
- `worldbank01.external_dev_stats.trade_country_latest`

### Main columns
- `reporter_name`
- `reporter_iso3`
- `year`
- `hs_code`
- `hs_label`
- `flow_code`
- `flow_name`
- `partner_code`
- `partner_name`
- `trade_value_usd`
- `net_weight_kg`
- `source_name`
- `load_timestamp`

---

## 10) City temperature pipeline
This workflow retrieves historical daily temperature data from **Open-Meteo** for a selected group of major world cities and converts them into annual city-level averages.

### Cities currently included
- Tokyo
- New York City
- London
- São Paulo
- Accra
- Nairobi
- Jakarta
- Almaty

### Source
- Open-Meteo Historical Weather API

### Transformations
- retrieve daily mean temperature for each city
- aggregate daily values into annual mean temperature
- count the number of non-null observation days per city-year
- store results as city-year analytical tables

### Why this matters analytically
Although climate data is external to the World Bank API ecosystem, it can be used as a complementary contextual layer for:
- urban comparison
- environmental context
- future linking with socioeconomic indicators

### BigQuery table
Dataset:
- `external_dev_stats`

Table:
- `worldbank01.external_dev_stats.city_temperature_annual`

### Main columns
- `city_name`
- `country_name`
- `year`
- `latitude`
- `longitude`
- `avg_temp_c_annual`
- `observation_days`
- `source_name`
- `load_timestamp`

---

## 11) Big Mac Index pipeline
This workflow uses the **Big Mac Index** as a supplementary external proxy for price levels, purchasing power, and relative currency valuation.

### Source
- The Economist Big Mac Index

### Why this matters analytically
The Big Mac Index is not an official World Bank indicator.  
In this repository it is treated as a complementary external source for comparative price-level and purchasing-power context.

This makes it possible to compare:
- income levels and relative prices
- purchasing-power proxy and education / health indicators
- trade structure and price-level context

### Outputs
Two tables are created:

#### Country-period table
- historical country-period data

#### Latest country snapshot
- most recent non-null record for each country

### BigQuery tables
Dataset:
- `external_dev_stats`

Tables:
- `worldbank01.external_dev_stats.big_mac_index_country_period`
- `worldbank01.external_dev_stats.big_mac_index_country_latest`

### Main columns
- `country_name`
- `country_iso`
- `date`
- `year`
- `currency_code`
- `local_price`
- `dollar_price`
- `usd_raw_index`
- `usd_adjusted_index`
- `gdp_dollar`
- `source_name`
- `load_timestamp`

---

## Validation vs testing

### Validation
Validation checks the **current transformed dataset** before loading.

Examples:
- missing required columns
- null country or year identifiers
- duplicate country-year rows
- null-heavy value columns
- unusual year ranges

Validation returns:
- **errors** → stop the pipeline
- **warnings** → log and continue

### Testing
Testing checks whether the **code logic** behaves as expected.

Examples:
- interpolation behaves correctly
- annualization logic works correctly
- latest-value extraction returns the correct row
- trade transformation returns the expected country-year record
- climate aggregation returns the correct annual summary
- governance dimension pivoting works correctly
- FAS series-code mapping works correctly
- Global Findex curated variable mapping works correctly

Tests are implemented with `pytest`.

---

## BigQuery loading
All current loads use:

- `WRITE_TRUNCATE`

This means destination tables are fully refreshed on each run.

---

## Raw data landing convention

Some workflows read directly from APIs, while others intentionally use manually downloaded source files in a raw landing area.

### Raw landing folder
```text
data/
└── raw/
```

- Current manually landed raw files
data/raw/global_findex_country.csv
data/raw/imf_fas.csv
data/raw/wgi.xlsx

- This design is intentional for source files whose download links, packaging, or bulk export formats may change over time.  
Raw source files are intentionally not tracked in Git due to file size and source-distribution considerations. Place them manually in `data/raw/` before running the pipelines.

## Repository structure
wb_dev_data_pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── pytest.ini
├── src/
│   ├── __init__.py
│   ├── main_u5mr.py
│   ├── extract_u5mr.py
│   ├── transform_u5mr.py
│   ├── main_girls_primary_completion.py
│   ├── extract_girls_primary_completion.py
│   ├── transform_girls_primary_completion.py
│   ├── main_gdp_per_capita.py
│   ├── extract_gdp_per_capita.py
│   ├── transform_gdp_per_capita.py
│   ├── main_oda_per_capita.py
│   ├── extract_oda_per_capita.py
│   ├── transform_oda_per_capita.py
│   ├── main_lays.py
│   ├── extract_lays.py
│   ├── transform_lays.py
│   ├── main_wgi.py
│   ├── extract_wgi.py
│   ├── transform_wgi.py
│   ├── main_global_findex.py
│   ├── extract_global_findex.py
│   ├── transform_global_findex.py
│   ├── main_imf_fas.py
│   ├── extract_imf_fas.py
│   ├── transform_imf_fas.py
│   ├── main_trade.py
│   ├── extract_trade.py
│   ├── transform_trade.py
│   ├── main_city_temperature.py
│   ├── extract_city_temperature.py
│   ├── transform_city_temperature.py
│   ├── main_big_mac.py
│   ├── extract_big_mac.py
│   ├── transform_big_mac.py
│   ├── validate.py
│   ├── load_bigquery.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_transform_u5mr.py
│   ├── test_transform_girls_primary_completion.py
│   ├── test_transform_gdp_per_capita.py
│   ├── test_transform_lays.py
│   ├── test_transform_wgi.py
│   ├── test_transform_global_findex.py
│   ├── test_transform_imf_fas.py
│   ├── test_transform_trade.py
│   ├── test_transform_city_temperature.py
│   ├── test_transform_big_mac.py
├── sql/
│   ├── create_dataset.sql
│   ├── create_tables_u5mr.sql
│   ├── create_tables_girls_primary_completion.sql
│   ├── create_tables_gdp_per_capita.sql
│   ├── create_tables_oda_per_capita.sql
│   ├── create_tables_lays.sql
│   ├── create_tables_wgi.sql
│   ├── create_tables_global_findex.sql
│   ├── create_tables_imf_fas.sql
│   ├── create_tables_trade.sql
│   ├── create_tables_city_temperature.sql
│   ├── create_tables_big_mac.sql
│   └── sample_queries.sql
├── data/
│   └── raw/
├── outputs/
│   ├── charts/
│   └── tables/
└── .github/
    └── workflows/
        └── ci.yml