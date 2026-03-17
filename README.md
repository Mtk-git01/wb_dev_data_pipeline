# wb_dev_data_pipeline

Reproducible ETL pipelines for public development indicators, with validation, BigQuery loading, and analysis-ready country-year outputs.

## Overview
This repository builds development-data pipelines that:

- extract public international indicator data
- transform raw inputs into country-year analytical tables
- validate structural and data-quality conditions
- load curated outputs into BigQuery
- support downstream cross-country analysis and visualization

Current implemented pipelines:

- **Under-five mortality (U5MR)** from **UN-IGME**
- **Girls’ primary completion rate** from the **World Bank API**
- **Trade flows** from **UN Comtrade**

---

## Why this repository
This project is designed to demonstrate:

- source-oriented data extraction
- reproducible ETL design
- country-year data modeling
- explicit data lineage awareness
- validation before loading
- cloud-ready analytical storage in BigQuery
- the ability to transform source statistical inputs into curated analytical assets

---

## Current pipelines

### 1) U5MR pipeline
The U5MR workflow uses the **UN-IGME observational database** as the upstream source, rather than relying only on downstream redistribution through World Bank Open Data.

This reflects an explicit **data lineage** choice:
- use the original source-side dataset
- treat it as the **source-of-truth raw input**
- transform it into an analysis-ready annual country-year table

#### U5MR transformations
- filter to included observations
- convert irregular observation dates into annual records
- aggregate multiple observations within the same year
- standardize to **one row per country per year**
- fill missing internal years using **linear interpolation**
- flag interpolated years using `is_interpolated`

#### Linear interpolation
If observed values are available at:
- year `t0` with value `y0`
- year `t1` with value `y1`

then the estimated value at an intermediate year `t` is:

\[
\hat{y}= y_0 + (y_1-y_0)\frac{t-t_0}{t_1-t_0}
\]

This converts irregularly spaced observations into a continuous annual analytical series.

#### Important note
The U5MR table in this repository is **not the official UN-IGME modelled estimate series**.  
It is an **annualized and interpolated analytical table** derived from the underlying observational source data.

#### BigQuery table
- `worldbank01.wb_dev_stats.u5mr_country_year`

#### Main columns
- `country_name`
- `country_iso`
- `year`
- `u5mr_estimate`
- `standard_error_of_estimates`
- `is_interpolated`

---

### 2) Girls’ primary completion pipeline
This workflow retrieves:

- **Primary completion rate, female (% of relevant age group)**
- Indicator code: `SE.PRM.CMPT.FE.ZS`

#### Source
- **World Bank API**

#### Outputs
Two BigQuery tables are created:

**Country-year table**
- full country-year time series
- useful for trend analysis and panel joins

**Latest country snapshot**
- most recent non-null value for each country
- useful for cross-country comparison and ranking

#### BigQuery tables
- `worldbank01.wb_dev_stats.girls_primary_completion_country_year`
- `worldbank01.wb_dev_stats.girls_primary_completion_country_latest`

---

### 3) Trade pipeline
This repository also includes a trade-data workflow built from **UN Comtrade**, chosen as a more source-oriented and raw-data-near input for international merchandise trade analysis.

This reflects a deliberate **data lineage** choice:
- instead of relying only on downstream summary tables
- the workflow retrieves trade records from **UN Comtrade**
- and transforms them into analysis-ready country-year trade tables for downstream statistical use

#### Why UN Comtrade
UN Comtrade is treated here as a **primary-data-near trade source** for internationally reported merchandise trade flows.  
Using this source makes it possible to work closer to the original reporting structure of trade statistics before transforming them into curated analytical tables.

This is important for:
- traceable data lineage
- source transparency
- reproducible extraction logic
- consistent transformation into country-year statistical assets

#### Current trade scope
The current implementation focuses on a small, interpretable set of country-product-flow combinations chosen to support development-oriented analysis.

**Luxury goods / high-end consumption proxy**
- Jewellery imports
  - Japan
  - Kazakhstan

**Developing-country-origin commodity exports**
- Coffee exports
  - Brazil
  - Ghana
- Cocoa exports
  - Brazil
  - Ghana

This design allows the trade module to capture both:
- **high-value consumption-oriented trade**
- **commodity exports linked to developing-country production structures**

#### Trade transformations
The trade workflow:
- retrieves annual trade data from UN Comtrade
- keeps the extraction layer relatively close to the raw source structure
- selects essential reporting fields for analytical use
- standardizes outputs into country-year records
- loads curated outputs into BigQuery

The curated trade tables use:
- `primaryValue` from source data as `trade_value_usd`
- `netWgt` from source data as `net_weight_kg`

#### Why this matters analytically
This trade pipeline is designed not as a standalone trade exercise, but as a module that can be joined with other development indicators already included in the repository, such as:

- under-five mortality (U5MR)
- girls’ primary completion rate
- future extensions such as fertility, GDP per capita, and ODA-related indicators

This makes it possible to study development-relevant relationships between:
- export structure and human development
- commodity dependence and social indicators
- high-end import exposure and economic development level
- trade patterns and broader country trajectories

#### Trade output tables
BigQuery tables:
- `worldbank01.wb_dev_stats.trade_country_year_long`
- `worldbank01.wb_dev_stats.trade_country_latest`

#### Main columns
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

## Validation vs testing

### Validation
Validation checks the **current transformed dataset** before loading.

Examples:
- missing required columns
- null `country_iso`
- null `year`
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

Tests are implemented with `pytest`.

---

## BigQuery loading
All current loads use:

- `WRITE_TRUNCATE`

This means destination tables are **fully refreshed on each run**.

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
│   ├── main_trade.py
│   ├── extract_trade.py
│   ├── transform_trade.py
│   ├── validate.py
│   ├── load_bigquery.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_transform_u5mr.py
│   ├── test_transform_girls_primary_completion.py
│   └── test_transform_trade.py
├── sql/
│   ├── create_dataset.sql
│   ├── create_tables_u5mr.sql
│   ├── create_tables_girls_primary_completion.sql
│   ├── create_tables_trade.sql
│   └── sample_queries.sql
├── outputs/
│   ├── charts/
│   └── tables/
└── .github/
    └── workflows/
        └── ci.yml