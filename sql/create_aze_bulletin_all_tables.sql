
-- Bronze tables
CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_business_portfolio_periodic_raw` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  business_loans_total_mn_azn FLOAT64,
  large_business_loans_mn_azn FLOAT64,
  medium_business_loans_mn_azn FLOAT64,
  small_business_loans_mn_azn FLOAT64,
  micro_business_loans_mn_azn FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_sectoral_loans_periodic_raw` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  real_sector_loans_total_mn_azn FLOAT64,
  real_sector_overdue_loans_mn_azn FLOAT64,
  real_sector_overdue_share_pct FLOAT64,
  trade_and_services_loans_mn_azn FLOAT64,
  mining_utilities_loans_mn_azn FLOAT64,
  agriculture_loans_mn_azn FLOAT64,
  construction_loans_mn_azn FLOAT64,
  industry_manufacturing_loans_mn_azn FLOAT64,
  transport_communication_loans_mn_azn FLOAT64,
  households_loans_mn_azn FLOAT64,
  real_estate_mortgage_loans_mn_azn FLOAT64,
  other_sectors_loans_mn_azn FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_national_payment_systems_periodic_raw` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  rtgs_txn_count_thousand FLOAT64,
  rtgs_txn_amount_mn_azn FLOAT64,
  rtgs_avg_amount_thousand_azn FLOAT64,
  lvpcss_txn_count_thousand FLOAT64,
  lvpcss_txn_amount_mn_azn FLOAT64,
  lvpcss_avg_amount_azn FLOAT64,
  ips_txn_count_thousand FLOAT64,
  ips_txn_amount_mn_azn FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_payment_service_monthly_raw` (
  country_name STRING,
  country_iso STRING,
  month DATE,
  atm_total_units FLOAT64,
  atm_baku_units FLOAT64,
  atm_regions_units FLOAT64,
  pos_total_units FLOAT64,
  contactless_pos_total_units FLOAT64,
  retail_service_pos_total_units FLOAT64,
  retail_service_pos_baku_units FLOAT64,
  baku_pos_total_units FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_card_transactions_monthly_raw` (
  country_name STRING,
  country_iso STRING,
  month DATE,
  payment_cards_total_thousand FLOAT64,
  payment_cards_contactless_thousand FLOAT64,
  debit_social_cards_thousand FLOAT64,
  debit_salary_cards_thousand FLOAT64,
  debit_other_cards_thousand FLOAT64,
  credit_cards_thousand FLOAT64,
  card_txn_count_thousand FLOAT64,
  card_txn_amount_mn_azn FLOAT64,
  cash_withdrawal_atm_count_thousand FLOAT64,
  cash_withdrawal_atm_amount_mn_azn FLOAT64,
  cash_withdrawal_pos_count_thousand FLOAT64,
  cash_withdrawal_pos_amount_mn_azn FLOAT64,
  non_cash_atm_count_thousand FLOAT64,
  non_cash_atm_amount_mn_azn FLOAT64,
  non_cash_pos_count_thousand FLOAT64,
  non_cash_pos_amount_mn_azn FLOAT64,
  contactless_pos_count_thousand FLOAT64,
  contactless_pos_amount_mn_azn FLOAT64,
  ecommerce_count_thousand FLOAT64,
  ecommerce_amount_mn_azn FLOAT64,
  self_service_terminal_count_thousand FLOAT64,
  self_service_terminal_amount_mn_azn FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_customer_accounts_ebanking_monthly_raw` (
  country_name STRING,
  country_iso STRING,
  month DATE,
  bank_customers_total_people FLOAT64,
  bank_customers_individuals_people FLOAT64,
  bank_customers_individual_entrepreneurs_people FLOAT64,
  bank_customers_legal_entities_people FLOAT64,
  customer_accounts_total_count FLOAT64,
  customer_accounts_transaction_count FLOAT64,
  customer_accounts_credit_count FLOAT64,
  customer_accounts_deposit_count FLOAT64,
  transaction_accounts_individuals_count FLOAT64,
  transaction_accounts_individual_entrepreneurs_count FLOAT64,
  transaction_accounts_legal_entities_count FLOAT64,
  internet_banking_users_count FLOAT64,
  internet_banking_legal_entities_count FLOAT64,
  mobile_banking_users_count FLOAT64,
  mobile_banking_legal_entities_count FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_macro_main_periodic_raw` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  nominal_gdp_mn_azn FLOAT64,
  real_gdp_growth_pct FLOAT64,
  gdp_deflator_pct FLOAT64,
  non_oil_gdp_mn_azn FLOAT64,
  non_oil_gdp_growth_pct FLOAT64,
  capital_investment_mn_azn FLOAT64,
  capital_investment_growth_pct FLOAT64,
  nominal_income_mn_azn FLOAT64,
  nominal_income_growth_pct FLOAT64,
  avg_monthly_wage_azn FLOAT64,
  avg_monthly_wage_growth_pct FLOAT64,
  cpi_monthly_pct FLOAT64,
  cpi_12m_pct FLOAT64,
  cpi_annual_avg_pct FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_balance_of_payments_periodic_raw` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  current_account_balance_mn_usd FLOAT64,
  trade_balance_mn_usd FLOAT64,
  goods_exports_total_mn_usd FLOAT64,
  oil_gas_exports_mn_usd FLOAT64,
  other_exports_mn_usd FLOAT64,
  goods_imports_total_mn_usd FLOAT64,
  oil_gas_imports_mn_usd FLOAT64,
  other_imports_mn_usd FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_foreign_trade_periodic_raw` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  total_exports_ths_usd FLOAT64,
  exports_yoy_pct FLOAT64,
  exports_non_cis_ths_usd FLOAT64,
  exports_non_cis_yoy_pct FLOAT64,
  exports_cis_ths_usd FLOAT64,
  exports_cis_yoy_pct FLOAT64,
  total_imports_ths_usd FLOAT64,
  imports_yoy_pct FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_movable_property_registry_periodic_raw` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  notices_entered_count FLOAT64,
  searches_count FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_npl_structure_periodic_raw` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  npl_total_mn_azn FLOAT64,
  npl_business_mn_azn FLOAT64,
  npl_consumer_mn_azn FLOAT64,
  npl_mortgage_mn_azn FLOAT64,
  npl_ratio_pct FLOAT64,
  npl_business_ratio_pct FLOAT64,
  npl_consumer_ratio_pct FLOAT64,
  npl_mortgage_ratio_pct FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_bronze.aze_interest_rates_periodic_raw` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  deposit_avg_rate_azn_pct FLOAT64,
  deposit_legal_rate_azn_pct FLOAT64,
  deposit_individual_rate_azn_pct FLOAT64,
  loan_avg_rate_azn_pct FLOAT64,
  loan_legal_rate_azn_pct FLOAT64,
  loan_individual_rate_azn_pct FLOAT64,
  deposit_avg_rate_fx_pct FLOAT64,
  deposit_legal_rate_fx_pct FLOAT64,
  deposit_individual_rate_fx_pct FLOAT64,
  loan_avg_rate_fx_pct FLOAT64,
  loan_legal_rate_fx_pct FLOAT64,
  loan_individual_rate_fx_pct FLOAT64,
  source_file STRING,
  bulletin_period DATE
);

-- Silver tables
CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_business_portfolio_periodic` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_business_portfolio_periodic_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_sectoral_loans_periodic` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_sectoral_loans_periodic_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_national_payment_systems_periodic` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_national_payment_systems_periodic_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_payment_service_monthly` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_payment_service_monthly_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_card_transactions_monthly` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_card_transactions_monthly_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_customer_accounts_ebanking_monthly` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_customer_accounts_ebanking_monthly_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_macro_main_periodic` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_macro_main_periodic_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_balance_of_payments_periodic` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_balance_of_payments_periodic_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_foreign_trade_periodic` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_foreign_trade_periodic_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_movable_property_registry_periodic` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_movable_property_registry_periodic_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_npl_structure_periodic` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_npl_structure_periodic_raw` WHERE 1=0;

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats_silver.aze_interest_rates_periodic` AS
SELECT *, CAST(NULL AS STRING) AS source_name, CURRENT_TIMESTAMP() AS load_timestamp
FROM `worldbank01.external_dev_stats_bronze.aze_interest_rates_periodic_raw` WHERE 1=0;

-- Gold marts
CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.aze_credit_access_and_stability_periodic` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  business_loans_total_mn_azn FLOAT64,
  large_business_loans_mn_azn FLOAT64,
  medium_business_loans_mn_azn FLOAT64,
  small_business_loans_mn_azn FLOAT64,
  micro_business_loans_mn_azn FLOAT64,
  real_sector_loans_total_mn_azn FLOAT64,
  real_sector_overdue_loans_mn_azn FLOAT64,
  real_sector_overdue_share_pct FLOAT64,
  trade_and_services_loans_mn_azn FLOAT64,
  mining_utilities_loans_mn_azn FLOAT64,
  agriculture_loans_mn_azn FLOAT64,
  construction_loans_mn_azn FLOAT64,
  industry_manufacturing_loans_mn_azn FLOAT64,
  transport_communication_loans_mn_azn FLOAT64,
  households_loans_mn_azn FLOAT64,
  real_estate_mortgage_loans_mn_azn FLOAT64,
  other_sectors_loans_mn_azn FLOAT64,
  npl_total_mn_azn FLOAT64,
  npl_business_mn_azn FLOAT64,
  npl_consumer_mn_azn FLOAT64,
  npl_mortgage_mn_azn FLOAT64,
  npl_ratio_pct FLOAT64,
  npl_business_ratio_pct FLOAT64,
  npl_consumer_ratio_pct FLOAT64,
  npl_mortgage_ratio_pct FLOAT64,
  deposit_avg_rate_azn_pct FLOAT64,
  deposit_legal_rate_azn_pct FLOAT64,
  deposit_individual_rate_azn_pct FLOAT64,
  loan_avg_rate_azn_pct FLOAT64,
  loan_legal_rate_azn_pct FLOAT64,
  loan_individual_rate_azn_pct FLOAT64,
  deposit_avg_rate_fx_pct FLOAT64,
  deposit_legal_rate_fx_pct FLOAT64,
  deposit_individual_rate_fx_pct FLOAT64,
  loan_avg_rate_fx_pct FLOAT64,
  loan_legal_rate_fx_pct FLOAT64,
  loan_individual_rate_fx_pct FLOAT64,
  notices_entered_count FLOAT64,
  searches_count FLOAT64,
  source_name STRING,
  load_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.aze_digital_finance_periodic` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  rtgs_txn_count_thousand FLOAT64,
  rtgs_txn_amount_mn_azn FLOAT64,
  rtgs_avg_amount_thousand_azn FLOAT64,
  lvpcss_txn_count_thousand FLOAT64,
  lvpcss_txn_amount_mn_azn FLOAT64,
  lvpcss_avg_amount_azn FLOAT64,
  ips_txn_count_thousand FLOAT64,
  ips_txn_amount_mn_azn FLOAT64,
  atm_total_units FLOAT64,
  atm_baku_units FLOAT64,
  atm_regions_units FLOAT64,
  pos_total_units FLOAT64,
  contactless_pos_total_units FLOAT64,
  retail_service_pos_total_units FLOAT64,
  retail_service_pos_baku_units FLOAT64,
  baku_pos_total_units FLOAT64,
  payment_cards_total_thousand FLOAT64,
  payment_cards_contactless_thousand FLOAT64,
  debit_social_cards_thousand FLOAT64,
  debit_salary_cards_thousand FLOAT64,
  debit_other_cards_thousand FLOAT64,
  credit_cards_thousand FLOAT64,
  card_txn_count_thousand FLOAT64,
  card_txn_amount_mn_azn FLOAT64,
  cash_withdrawal_atm_count_thousand FLOAT64,
  cash_withdrawal_atm_amount_mn_azn FLOAT64,
  cash_withdrawal_pos_count_thousand FLOAT64,
  cash_withdrawal_pos_amount_mn_azn FLOAT64,
  non_cash_atm_count_thousand FLOAT64,
  non_cash_atm_amount_mn_azn FLOAT64,
  non_cash_pos_count_thousand FLOAT64,
  non_cash_pos_amount_mn_azn FLOAT64,
  contactless_pos_count_thousand FLOAT64,
  contactless_pos_amount_mn_azn FLOAT64,
  ecommerce_count_thousand FLOAT64,
  ecommerce_amount_mn_azn FLOAT64,
  self_service_terminal_count_thousand FLOAT64,
  self_service_terminal_amount_mn_azn FLOAT64,
  bank_customers_total_people FLOAT64,
  bank_customers_individuals_people FLOAT64,
  bank_customers_individual_entrepreneurs_people FLOAT64,
  bank_customers_legal_entities_people FLOAT64,
  customer_accounts_total_count FLOAT64,
  customer_accounts_transaction_count FLOAT64,
  customer_accounts_credit_count FLOAT64,
  customer_accounts_deposit_count FLOAT64,
  transaction_accounts_individuals_count FLOAT64,
  transaction_accounts_individual_entrepreneurs_count FLOAT64,
  transaction_accounts_legal_entities_count FLOAT64,
  internet_banking_users_count FLOAT64,
  internet_banking_legal_entities_count FLOAT64,
  mobile_banking_users_count FLOAT64,
  mobile_banking_legal_entities_count FLOAT64,
  source_name STRING,
  load_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `worldbank01.external_dev_stats.aze_economic_diversification_periodic` (
  country_name STRING,
  country_iso STRING,
  period_date DATE,
  period_type STRING,
  nominal_gdp_mn_azn FLOAT64,
  real_gdp_growth_pct FLOAT64,
  gdp_deflator_pct FLOAT64,
  non_oil_gdp_mn_azn FLOAT64,
  non_oil_gdp_growth_pct FLOAT64,
  capital_investment_mn_azn FLOAT64,
  capital_investment_growth_pct FLOAT64,
  nominal_income_mn_azn FLOAT64,
  nominal_income_growth_pct FLOAT64,
  avg_monthly_wage_azn FLOAT64,
  avg_monthly_wage_growth_pct FLOAT64,
  cpi_monthly_pct FLOAT64,
  cpi_12m_pct FLOAT64,
  cpi_annual_avg_pct FLOAT64,
  current_account_balance_mn_usd FLOAT64,
  trade_balance_mn_usd FLOAT64,
  goods_exports_total_mn_usd FLOAT64,
  oil_gas_exports_mn_usd FLOAT64,
  other_exports_mn_usd FLOAT64,
  goods_imports_total_mn_usd FLOAT64,
  oil_gas_imports_mn_usd FLOAT64,
  other_imports_mn_usd FLOAT64,
  total_exports_ths_usd FLOAT64,
  exports_yoy_pct FLOAT64,
  exports_non_cis_ths_usd FLOAT64,
  exports_non_cis_yoy_pct FLOAT64,
  exports_cis_ths_usd FLOAT64,
  exports_cis_yoy_pct FLOAT64,
  total_imports_ths_usd FLOAT64,
  imports_yoy_pct FLOAT64,
  source_name STRING,
  load_timestamp TIMESTAMP
);

-- Convenience latest views
CREATE OR REPLACE VIEW `worldbank01.external_dev_stats.aze_credit_access_and_stability_latest` AS
SELECT *
FROM `worldbank01.external_dev_stats.aze_credit_access_and_stability_periodic`
QUALIFY ROW_NUMBER() OVER (PARTITION BY country_iso ORDER BY period_date DESC) = 1;

CREATE OR REPLACE VIEW `worldbank01.external_dev_stats.aze_digital_finance_latest` AS
SELECT *
FROM `worldbank01.external_dev_stats.aze_digital_finance_periodic`
QUALIFY ROW_NUMBER() OVER (PARTITION BY country_iso ORDER BY period_date DESC) = 1;

CREATE OR REPLACE VIEW `worldbank01.external_dev_stats.aze_economic_diversification_latest` AS
SELECT *
FROM `worldbank01.external_dev_stats.aze_economic_diversification_periodic`
QUALIFY ROW_NUMBER() OVER (PARTITION BY country_iso ORDER BY period_date DESC) = 1;
