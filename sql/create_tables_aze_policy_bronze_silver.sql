CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_policy_rate_events_raw` (
    effective_date DATE,
    refinancing_rate FLOAT64,
    corridor_floor FLOAT64,
    corridor_ceiling FLOAT64,
    source_url STRING
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_policy_rate_monthly` (
    month DATE,
    refinancing_rate FLOAT64,
    corridor_floor FLOAT64,
    corridor_ceiling FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);