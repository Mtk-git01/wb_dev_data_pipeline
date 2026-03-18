# wb_dev_data_pipeline

Reproducible ETL pipelines for public development indicators, trade statistics, and climate-related external data, with validation, BigQuery loading, and analysis-ready outputs.

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

### External source-oriented datasets
- Under-five mortality (U5MR) from UN-IGME
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
- **official API-based World Bank indicators**
- **external public datasets used as complementary analytical inputs**

To reflect this, BigQuery tables are organized into two datasets:

- `wb_dev_stats`  
  for World Bank API-derived tables

- `external_dev_stats`  
  for external datasets such as UN-IGME, UN Comtrade, Open-Meteo, and Big Mac Index

---

## BigQuery datasets

### 1) World Bank API-derived dataset
Dataset:
- `worldbank01.wb_dev_stats`

This dataset contains indicators retrieved directly from the World Bank API.

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
If observed values are available at:
- year `t0` with value `y0`
- year `t1` with value `y1`

then the estimated value at an intermediate year `t` is:

\[
\hat{y}= y_0 + (y_1-y_0)\frac{t-t_0}{t_1-t_0}
\]

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
- useful for panel analysis and joins with education, health, aid, and trade indicators

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

## 6) Trade pipeline
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

## 7) City temperature pipeline
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

## 8) Big Mac Index pipeline
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

Tests are implemented with `pytest`.

---

## BigQuery loading
All current loads use:

- `WRITE_TRUNCATE`

This means destination tables are fully refreshed on each run.

---

## Repository structure
```text
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
│   ├── test_transform_trade.py
│   ├── test_transform_city_temperature.py
│   ├── test_transform_big_mac.py
│   └── test_transform_lays.py
├── sql/
│   ├── create_dataset.sql
│   ├── create_tables_u5mr.sql
│   ├── create_tables_girls_primary_completion.sql
│   ├── create_tables_gdp_per_capita.sql
│   ├── create_tables_oda_per_capita.sql
│   ├── create_tables_lays.sql
│   ├── create_tables_trade.sql
│   ├── create_tables_city_temperature.sql
│   ├── create_tables_big_mac.sql
│   └── sample_queries.sql
├── outputs/
│   ├── charts/
│   └── tables/
└── .github/
    └── workflows/
        └── ci.yml