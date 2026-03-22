CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.aze_fx_daily_raw` (
    as_of_date DATE,
    currency_name STRING,
    currency_code STRING,
    nominal FLOAT64,
    rate_azn FLOAT64,
    rate_azn_per_unit FLOAT64
);