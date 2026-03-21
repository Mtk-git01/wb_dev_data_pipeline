CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.imf_fas_country_year` (
    country_name STRING,
    country_iso STRING,
    year INT64,
    commercial_banks_number FLOAT64,
    borrowers_commercial_banks_number FLOAT64,
    active_mobile_money_accounts_number FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.imf_fas_country_latest` (
    country_name STRING,
    country_iso STRING,
    year INT64,
    commercial_banks_number FLOAT64,
    borrowers_commercial_banks_number FLOAT64,
    active_mobile_money_accounts_number FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);