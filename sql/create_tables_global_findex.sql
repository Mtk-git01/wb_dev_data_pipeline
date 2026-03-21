CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.global_findex_country_year` (
    country_name STRING,
    country_iso STRING,
    year INT64,
    account_ownership_pct FLOAT64,
    financial_institution_account_pct FLOAT64,
    mobile_money_account_pct FLOAT64,
    digital_payment_pct FLOAT64,
    borrowed_from_financial_institution_pct FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.global_findex_country_latest` (
    country_name STRING,
    country_iso STRING,
    year INT64,
    account_ownership_pct FLOAT64,
    financial_institution_account_pct FLOAT64,
    mobile_money_account_pct FLOAT64,
    digital_payment_pct FLOAT64,
    borrowed_from_financial_institution_pct FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);