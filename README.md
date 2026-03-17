# wb_dev_data_pipeline

A reproducible cross-country development data pipeline for public international indicators.

## Project overview
This repository is designed to extract, transform, validate, and store country-year development indicators from multiple public sources. The goal is to build a harmonized analytical dataset that can support downstream statistical analysis, visualization, and policy-oriented interpretation.

## Current scope
The initial version focuses on:
- Under-five mortality
- Fertility
- Population

The pipeline is designed to be extensible so that additional indicators such as GDP per capita, life expectancy, education, and gender-related variables can be added later.

## Objectives
- Build a reproducible ETL workflow for development indicators
- Harmonize data into a country-year panel structure
- Apply basic data-quality checks and interpolation where appropriate
- Load curated outputs into BigQuery
- Support future cross-country analysis and visualization

## Repository structure
```text
wb_dev_data_pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── pytest.ini
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load_bigquery.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_transform.py
│   └── test_validate.py
├── sql/
│   ├── create_dataset.sql
│   ├── create_views.sql
│   └── sample_queries.sql
├── outputs/
│   ├── charts/
│   └── tables/
└── .github/
    └── workflows/
        └── ci.yml