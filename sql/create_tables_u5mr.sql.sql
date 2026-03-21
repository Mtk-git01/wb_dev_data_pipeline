CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.u5mr_country_year` (
  country_name STRING,
  country_iso STRING,
  year INT64,
  u5mr_estimate FLOAT64,
  standard_error_of_estimates FLOAT64,
  is_interpolated BOOL
);