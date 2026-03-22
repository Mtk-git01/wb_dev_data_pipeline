CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_banking_monthly_raw` (
    month DATE,
    bank_total_assets_mn_azn FLOAT64,
    bank_loans_customers_mn_azn FLOAT64,
    bank_deposits_total_mn_azn FLOAT64
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_banking_monthly` (
    month DATE,
    bank_total_assets_mn_azn FLOAT64,
    bank_loans_customers_mn_azn FLOAT64,
    bank_deposits_total_mn_azn FLOAT64,
    source_name STRING,
    load_timestamp TIMESTAMP
);