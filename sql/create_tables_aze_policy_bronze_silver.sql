CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_policy_rate_events_raw` (
    month DATE,
    corridor_floor FLOAT64,
    refinancing_rate FLOAT64,
    corridor_ceiling FLOAT64,
    source_file STRING,
    bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_policy_rate_monthly` (
    month DATE,
    corridor_floor FLOAT64,
    refinancing_rate FLOAT64,
    corridor_ceiling FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);