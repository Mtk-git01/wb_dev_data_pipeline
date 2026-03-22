CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_macro_monthly_raw` (
    month DATE,
    cpi_yoy FLOAT64,
    official_fx_reserves_usd_mn FLOAT64
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_macro_monthly` (
    month DATE,
    cpi_yoy FLOAT64,
    official_fx_reserves_usd_mn FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);