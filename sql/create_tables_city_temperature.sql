CREATE TABLE IF NOT EXISTS `worldbank01.external_wb_dev_stats.city_temperature_annual` (
  city_name STRING,
  country_name STRING,
  year INT64,
  latitude FLOAT64,
  longitude FLOAT64,
  source_name STRING,
  avg_temp_c_annual FLOAT64,
  observation_days INT64,
  load_timestamp TIMESTAMP
);