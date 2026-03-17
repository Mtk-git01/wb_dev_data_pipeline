CREATE TABLE IF NOT EXISTS `worldbank01.wb_dev_stats.girls_primary_completion_country_year` (
  country_name STRING,
  country_iso STRING,
  year INT64,
  value FLOAT64,
  indicator_code STRING,
  indicator_name STRING,
  obs_status STRING,
  decimal_places INT64,
  source_name STRING,
  load_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `worldbank01.wb_dev_stats.girls_primary_completion_country_latest` (
  country_name STRING,
  country_iso STRING,
  year INT64,
  value FLOAT64,
  indicator_code STRING,
  indicator_name STRING,
  obs_status STRING,
  decimal_places INT64,
  source_name STRING,
  load_timestamp TIMESTAMP
);