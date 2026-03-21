CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.trade_country_year_long` (
  reporter_name STRING,
  reporter_iso3 STRING,
  year INT64,
  hs_code STRING,
  hs_label STRING,
  flow_code STRING,
  flow_name STRING,
  partner_code STRING,
  partner_name STRING,
  trade_value_usd FLOAT64,
  net_weight_kg FLOAT64,
  source_name STRING,
  load_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.trade_country_latest` (
  reporter_name STRING,
  reporter_iso3 STRING,
  year INT64,
  hs_code STRING,
  hs_label STRING,
  flow_code STRING,
  flow_name STRING,
  partner_code STRING,
  partner_name STRING,
  trade_value_usd FLOAT64,
  net_weight_kg FLOAT64,
  source_name STRING,
  load_timestamp TIMESTAMP
);