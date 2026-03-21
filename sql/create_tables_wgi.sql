CREATE TABLE IF NOT EXISTS `worldbank01.wb_dev_stats.wgi_country_year` (
    country_name STRING,
    country_iso STRING,
    year INT64,
    voice_accountability FLOAT64,
    political_stability FLOAT64,
    government_effectiveness FLOAT64,
    regulatory_quality FLOAT64,
    rule_of_law FLOAT64,
    control_of_corruption FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `worldbank01.wb_dev_stats.wgi_country_latest` (
    country_name STRING,
    country_iso STRING,
    year INT64,
    voice_accountability FLOAT64,
    political_stability FLOAT64,
    government_effectiveness FLOAT64,
    regulatory_quality FLOAT64,
    rule_of_law FLOAT64,
    control_of_corruption FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);