CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.big_mac_index_country_period` (
  country_name STRING,
  country_iso STRING,
  date DATE,
  year INT64,
  currency_code STRING,
  local_price FLOAT64,
  dollar_price FLOAT64,
  usd_raw_index FLOAT64,
  usd_adjusted_index FLOAT64,
  gdp_dollar FLOAT64,
  source_name STRING,
  load_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.big_mac_index_country_latest` (
  country_name STRING,
  country_iso STRING,
  date DATE,
  year INT64,
  currency_code STRING,
  local_price FLOAT64,
  dollar_price FLOAT64,
  usd_raw_index FLOAT64,
  usd_adjusted_index FLOAT64,
  gdp_dollar FLOAT64,
  source_name STRING,
  load_timestamp TIMESTAMP
);