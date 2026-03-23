PROJECT_ID = "worldbank01"
DATASET_ID = "wb_dev_stats" # WB_
EXTERNAL_DATASET_ID = "external_dev_stats"


U5MR_TABLE_ID = "u5mr_country_year"
U5MR_URL = "https://childmortality.org/wp-content/uploads/2024/03/UNIGME-2024-Total-U5MR-IMR-and-NMR-database.xlsx"

#
GIRLS_PRIMARY_COMPLETION_TABLE_COUNTRY_YEAR = "girls_primary_completion_country_year"
GIRLS_PRIMARY_COMPLETION_TABLE_COUNTRY_LATEST = "girls_primary_completion_country_latest"
WB_API_BASE = "https://api.worldbank.org/v2"
GIRLS_PRIMARY_COMPLETION_INDICATOR_CODE = "SE.PRM.CMPT.FE.ZS"
GIRLS_PRIMARY_COMPLETION_INDICATOR_NAME = "Primary completion rate, female (% of relevant age group)"
GIRLS_PRIMARY_COMPLETION_SOURCE_NAME = "World Bank API"

#
TRADE_TABLE_COUNTRY_YEAR = "trade_country_year_long"
TRADE_TABLE_COUNTRY_LATEST = "trade_country_latest"

TRADE_SOURCE_NAME = "UN Comtrade"

# TRADE_TARGETS = [
#     {"reporter_iso3": "GHA", "reporter_name": "Ghana",      "hs_code": "0901", "hs_label": "Coffee",      "flow_code": "X", "flow_name": "Export"},
#     {"reporter_iso3": "GHA", "reporter_name": "Ghana",      "hs_code": "1801", "hs_label": "Cocoa beans", "flow_code": "X", "flow_name": "Export"},
#     {"reporter_iso3": "BRA", "reporter_name": "Brazil",     "hs_code": "0901", "hs_label": "Coffee",      "flow_code": "X", "flow_name": "Export"},
#     {"reporter_iso3": "BRA", "reporter_name": "Brazil",     "hs_code": "1801", "hs_label": "Cocoa beans", "flow_code": "X", "flow_name": "Export"},
#     {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "2709", "hs_label": "oils",        "flow_code": "X", "flow_name": "Export"},
#     {"reporter_iso3": "BRA", "reporter_name": "Brazil",     "hs_code": "7113", "hs_label": "Jewellery",   "flow_code": "M", "flow_name": "Import"},
#     {"reporter_iso3": "KAZ", "reporter_name": "Kazakhstan", "hs_code": "7113", "hs_label": "Jewellery",   "flow_code": "M", "flow_name": "Import"},
#     {"reporter_iso3": "JPN", "reporter_name": "Japan",      "hs_code": "7113", "hs_label": "Jewellery",   "flow_code": "M", "flow_name": "Import"},
#     {"reporter_iso3": "JPN", "reporter_name": "Japan",      "hs_code": "2709", "hs_label": "oils",        "flow_code": "M", "flow_name": "Import"}

#]

TRADE_TARGETS = [
    # Azerbaijan: core export structure and diversification
    {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "2709", "hs_label": "Crude petroleum oils", "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "2711", "hs_label": "Petroleum gas / natural gas", "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "0802", "hs_label": "Nuts", "flow_code": "X", "flow_name": "Export"},

    # Azerbaijan: transport / logistics / car-heavy urban economy / Middle Corridor
    {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "8703", "hs_label": "Passenger cars", "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "8704", "hs_label": "Goods vehicles / trucks", "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "8607", "hs_label": "Railway parts", "flow_code": "M", "flow_name": "Import"},

    # Azerbaijan: digital connectivity / energy transition
    {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "8517", "hs_label": "Telecom equipment", "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "8504", "hs_label": "Transformers / electrical equipment", "flow_code": "M", "flow_name": "Import"},

    # Kazakhstan: Middle Corridor / rail / logistics / road connectivity
    {"reporter_iso3": "KAZ", "reporter_name": "Kazakhstan", "hs_code": "2709", "hs_label": "Crude petroleum oils", "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "KAZ", "reporter_name": "Kazakhstan", "hs_code": "8703", "hs_label": "Passenger cars", "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "KAZ", "reporter_name": "Kazakhstan", "hs_code": "8704", "hs_label": "Goods vehicles / trucks", "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "KAZ", "reporter_name": "Kazakhstan", "hs_code": "8607", "hs_label": "Railway parts", "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "KAZ", "reporter_name": "Kazakhstan", "hs_code": "8429", "hs_label": "Construction machinery", "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "KAZ", "reporter_name": "Kazakhstan", "hs_code": "8517", "hs_label": "Telecom equipment", "flow_code": "M", "flow_name": "Import"},
]

TRADE_PARTNER_CODE = "0"
TRADE_PARTNER_NAME = "World"

TRADE_START_YEAR = 2006
TRADE_END_YEAR = 2025

ISO3_TO_NUMERIC = {
    "JPN": "392",
    "KAZ": "398",
    "BRA": "076",
    "GHA": "288",
    "AZE": "031"
}

#
ODA_PER_CAPITA_TABLE_COUNTRY_YEAR = "oda_received_per_capita_country_year"
ODA_PER_CAPITA_TABLE_COUNTRY_LATEST = "oda_received_per_capita_country_latest"

WB_API_BASE = "https://api.worldbank.org/v2"
ODA_PER_CAPITA_INDICATOR_CODE = "DT.ODA.ODAT.PC.ZS"
ODA_PER_CAPITA_INDICATOR_NAME = "Net ODA received per capita (current US$)"
ODA_PER_CAPITA_SOURCE_NAME = "World Bank API"

#
GDP_PC_TABLE_COUNTRY_YEAR = "gdp_per_capita_country_year"
GDP_PC_TABLE_COUNTRY_LATEST = "gdp_per_capita_country_latest"

GDP_PC_INDICATOR_CODE = "NY.GDP.PCAP.CD"
GDP_PC_INDICATOR_NAME = "GDP per capita (current US$)"
GDP_PC_SOURCE_NAME = "World Bank API"

#
CITY_TEMP_TABLE_ANNUAL = "city_temperature_annual"

CITY_TEMPERATURE_SOURCE_NAME = "Open-Meteo Historical Weather API"
CITY_TEMPERATURE_MODEL = "era5"

CITY_TEMPERATURE_CITIES = [
    {"city_name": "Tokyo", "country_name": "Japan", "latitude": 35.6762, "longitude": 139.6503},
    {"city_name": "New York City", "country_name": "United States", "latitude": 40.7128, "longitude": -74.0060},
    {"city_name": "London", "country_name": "United Kingdom", "latitude": 51.5072, "longitude": -0.1276},
    {"city_name": "São Paulo", "country_name": "Brazil", "latitude": -23.5505, "longitude": -46.6333},
    {"city_name": "Accra", "country_name": "Ghana", "latitude": 5.6037, "longitude": -0.1870},
    {"city_name": "Nairobi", "country_name": "Kenya", "latitude": -1.2864, "longitude": 36.8172},
    {"city_name": "Jakarta", "country_name": "Indonesia", "latitude": -6.2088, "longitude": 106.8456},
    {"city_name": "Almaty", "country_name": "Kazakhstan", "latitude": 43.2220, "longitude": 76.8512},
    {"city_name": "Baku", "country_name": "Azerbaijan", "latitude": 40.4093, "longitude": 49.8671}

]

CITY_TEMP_START_DATE = "1994-01-01"
CITY_TEMP_END_DATE = "2023-12-31"

#
LAYS_TABLE_COUNTRY_YEAR = "lays_country_year"
LAYS_TABLE_COUNTRY_LATEST = "lays_country_latest"

LAYS_INDICATOR_CODE = "HD.HCI.LAYS"
LAYS_INDICATOR_NAME = "Learning-adjusted years of schooling"
LAYS_SOURCE_NAME = "World Bank API"

#
BIG_MAC_TABLE_COUNTRY_PERIOD = "big_mac_index_country_period"
BIG_MAC_TABLE_COUNTRY_LATEST = "big_mac_index_country_latest"

BIG_MAC_SOURCE_NAME = "The Economist Big Mac Index"
BIG_MAC_CSV_URL = "https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/output-data/big-mac-full-index.csv"

#
GDP_PC_TABLE_COUNTRY_YEAR = "gdp_per_capita_country_year"
GDP_PC_TABLE_COUNTRY_LATEST = "gdp_per_capita_country_latest"

GDP_PC_INDICATOR_CODE = "NY.GDP.PCAP.CD"
GDP_PC_INDICATOR_NAME = "GDP per capita (current US$)"
GDP_PC_SOURCE_NAME = "World Bank API"

##
#
GLOBAL_FINDEX_TABLE_COUNTRY_YEAR = "global_findex_country_year"
GLOBAL_FINDEX_TABLE_COUNTRY_LATEST = "global_findex_country_latest"

GLOBAL_FINDEX_SOURCE_NAME = "World Bank Global Findex"
GLOBAL_FINDEX_RAW_PATH = "data/raw/GlobalFindexDatabase2025.csv"

# Curated indicators to keep from the raw Global Findex country file.
# These are example column names expected in the raw CSV after standardization.
# Update RAW_TO_TARGET mapping if the official file uses slightly different names.
GLOBAL_FINDEX_RAW_TO_TARGET = {
    "account_t_d": "account_ownership_pct",
    "fiaccount_t_d": "financial_institution_account_pct",
    "mobileaccount_t_d": "mobile_money_account_pct",
    "dig_acc": "digital_payment_pct",
    "borrow_any_t_d": "borrowed_from_financial_institution_pct",
}

#
IMF_FAS_TABLE_COUNTRY_YEAR = "imf_fas_country_year"
IMF_FAS_TABLE_COUNTRY_LATEST = "imf_fas_country_latest"

IMF_FAS_SOURCE_NAME = "IMF Financial Access Survey"
IMF_FAS_RAW_PATH = "data/raw/imf_fas.csv"

# IMF FAS bulk export (wide format) uses SERIES_CODE.
# We keep a curated subset and map series code -> target column.
IMF_FAS_SERIES_TO_TARGET = {
    "COMBANK": "commercial_banks_number",
    "FA21_COMBANK": "borrowers_commercial_banks_number",
    "FA63": "active_mobile_money_accounts_number",
}

#
WGI_TABLE_COUNTRY_YEAR = "wgi_country_year"
WGI_TABLE_COUNTRY_LATEST = "wgi_country_latest"

WGI_SOURCE_NAME = "World Bank Worldwide Governance Indicators"
WGI_RAW_PATH = "data/raw/wgi.xlsx"

#AZE
#
AZE_BANK_OPS_TABLE_MONTHLY = "aze_bank_ops_monthly"

AZE_BANK_OPS_SOURCE_NAME = "CBAR / State Statistics Committee / manual monthly integration"

AZE_FX_RATES_URL = "https://www.cbar.az/currency/rates?language=en"
AZE_POLICY_RATE_RAW_PATH = "data/raw/cbar_policy_rate_events.csv"
AZE_BANKING_MONTHLY_RAW_PATH = "data/raw/aze_banking_monthly.csv"
AZE_FX_MONTHLY_RAW_PATH = "data/raw/aze_fx_monthly.csv"

#### csv
AZE_FX_DAILY_RAW_TABLE = "aze_fx_daily_raw"
AZE_FX_MONTHLY_TABLE = "aze_fx_monthly"

# Azerbaijan layered datasets
AZE_BRONZE_DATASET_ID = "external_dev_stats_bronze"
AZE_SILVER_DATASET_ID = "external_dev_stats_silver"

# Azerbaijan macro monthly
AZE_MACRO_MONTHLY_RAW_TABLE = "aze_macro_monthly_raw"
AZE_MACRO_MONTHLY_TABLE = "aze_macro_monthly"

# Azerbaijan banking monthly
AZE_BANKING_MONTHLY_RAW_TABLE = "aze_banking_monthly_raw"
AZE_BANKING_MONTHLY_TABLE = "aze_banking_monthly"

# Azerbaijan policy rate
AZE_POLICY_RATE_EVENTS_RAW_TABLE = "aze_policy_rate_events_raw"
AZE_POLICY_RATE_MONTHLY_TABLE = "aze_policy_rate_monthly"

# Source names
AZE_MACRO_MONTHLY_SOURCE_NAME = "Azerbaijan SSC / CBAR monthly macro integration"
AZE_BANKING_MONTHLY_SOURCE_NAME = "CBAR banking monthly integration"
AZE_POLICY_RATE_SOURCE_NAME = "CBAR policy rate events"

# Raw file paths
AZE_MACRO_MONTHLY_RAW_PATH = "data/raw/aze_macro_monthly.csv"
AZE_BANKING_MONTHLY_RAW_PATH = "data/raw/aze_banking_monthly.csv"
AZE_POLICY_RATE_RAW_PATH = "data/raw/cbar_policy_rate_events.csv"

# Azerbaijan Gold mart
AZE_BANK_OPS_TABLE_MONTHLY = "aze_bank_ops_monthly"
#AZE_BANK_OPS_SOURCE_NAME = "CBAR / SSC / banking monthly integration"
#AZE_BANK_OPS_SOURCE_NAME = "SSC / CBAR monthly integrated bank ops mart"
AZE_BANK_OPS_SOURCE_NAME = "CBAR / SSC monthly macro-financial integration"

# Existing FX dynamic layer
AZE_FX_DAILY_RAW_TABLE = "aze_fx_daily_raw"
AZE_FX_MONTHLY_TABLE = "aze_fx_monthly"

###API
# Azerbaijan layered datasets
AZE_BRONZE_DATASET_ID = "external_dev_stats_bronze"
AZE_SILVER_DATASET_ID = "external_dev_stats_silver"

# Azerbaijan macro/policy tables
AZE_MACRO_MONTHLY_RAW_TABLE = "aze_macro_monthly_raw"
AZE_MACRO_MONTHLY_TABLE = "aze_macro_monthly"

AZE_POLICY_RATE_EVENTS_RAW_TABLE = "aze_policy_rate_events_raw"
AZE_POLICY_RATE_MONTHLY_TABLE = "aze_policy_rate_monthly"

AZE_MACRO_MONTHLY_SOURCE_NAME = "Azerbaijan SSC / CBAR monthly macro integration"
AZE_POLICY_RATE_SOURCE_NAME = "CBAR policy rate events"

# Existing Azerbaijan FX / gold
AZE_FX_DAILY_RAW_TABLE = "aze_fx_daily_raw"
AZE_FX_MONTHLY_TABLE = "aze_fx_monthly"
AZE_BANK_OPS_TABLE_MONTHLY = "aze_bank_ops_monthly"
AZE_BANK_OPS_SOURCE_NAME = "CBAR / SSC monthly integration"

# URLs
AZE_CBAR_RESERVES_URL_TEMPLATE = "https://www.cbar.az/infoblocks/money_reserve_usd?language=en&year={year}"
AZE_CBAR_REFINANCING_URL_TEMPLATE = "https://www.cbar.az/infoblocks/corridor_percent?language=en&year={year}"

# SSC monthly macro pages (English)
AZE_SSC_MACRO_URL_TEMPLATE = "https://www.stat.gov.az/news/macroeconomy.php?arxiv=1&lang=en&page={page}"
AZE_SSC_MACRO_URL_LIVE = "https://www.stat.gov.az/news/macroeconomy.php?lang=en&page=1"

# Azerbaijan banking monthly from XLSX bulletins
AZE_BANKING_BULLETIN_XLSX_RAW_DIR = "data/raw/aze_banking_bulletins_xlsx"
AZE_BANKING_MONTHLY_RAW_TABLE = "aze_banking_monthly_raw"
AZE_BANKING_MONTHLY_TABLE = "aze_banking_monthly"
AZE_BANKING_MONTHLY_SOURCE_NAME = "CBAR Statistical Bulletin Table 5.2 (XLSX)"

# Azerbaijan policy monthly from XLSX bulletins
AZE_POLICY_BULLETIN_XLSX_RAW_DIR = "data/raw/aze_banking_bulletins_xlsx"
AZE_POLICY_RATE_EVENTS_RAW_TABLE = "aze_policy_rate_events_raw"
AZE_POLICY_RATE_MONTHLY_TABLE = "aze_policy_rate_monthly"
AZE_POLICY_RATE_SOURCE_NAME = "CBAR Statistical Bulletin Table 3.1 (XLSX)"

## Azerbaijan add tables

# Azerbaijan bulletin raw folder
AZE_BANKING_BULLETIN_XLSX_RAW_DIR = "data/raw/aze_banking_bulletins_xlsx"

# Bronze / Silver datasets
AZE_BRONZE_DATASET_ID = "external_dev_stats_bronze"
AZE_SILVER_DATASET_ID = "external_dev_stats_silver"

# Silver sources
AZE_BUSINESS_PORTFOLIO_PERIODIC_RAW_TABLE = "aze_business_portfolio_periodic_raw"
AZE_BUSINESS_PORTFOLIO_PERIODIC_TABLE = "aze_business_portfolio_periodic"
AZE_BUSINESS_PORTFOLIO_SOURCE_NAME = "CBAR statistical bulletin table 5.7"

AZE_SECTORAL_LOANS_PERIODIC_RAW_TABLE = "aze_sectoral_loans_periodic_raw"
AZE_SECTORAL_LOANS_PERIODIC_TABLE = "aze_sectoral_loans_periodic"
AZE_SECTORAL_LOANS_SOURCE_NAME = "CBAR statistical bulletin table 2.8"

AZE_NATIONAL_PAYMENT_SYSTEMS_PERIODIC_RAW_TABLE = "aze_national_payment_systems_periodic_raw"
AZE_NATIONAL_PAYMENT_SYSTEMS_PERIODIC_TABLE = "aze_national_payment_systems_periodic"
AZE_NATIONAL_PAYMENT_SYSTEMS_SOURCE_NAME = "CBAR statistical bulletin table 4.1"

AZE_PAYMENT_SERVICE_MONTHLY_RAW_TABLE = "aze_payment_service_monthly_raw"
AZE_PAYMENT_SERVICE_MONTHLY_TABLE = "aze_payment_service_monthly"
AZE_PAYMENT_SERVICE_MONTHLY_SOURCE_NAME = "CBAR statistical bulletin table 4.3"

AZE_CARD_TRANSACTIONS_MONTHLY_RAW_TABLE = "aze_card_transactions_monthly_raw"
AZE_CARD_TRANSACTIONS_MONTHLY_TABLE = "aze_card_transactions_monthly"
AZE_CARD_TRANSACTIONS_MONTHLY_SOURCE_NAME = "CBAR statistical bulletin table 4.5"

AZE_CUSTOMER_ACCOUNTS_EBANKING_MONTHLY_RAW_TABLE = "aze_customer_accounts_ebanking_monthly_raw"
AZE_CUSTOMER_ACCOUNTS_EBANKING_MONTHLY_TABLE = "aze_customer_accounts_ebanking_monthly"
AZE_CUSTOMER_ACCOUNTS_EBANKING_MONTHLY_SOURCE_NAME = "CBAR statistical bulletin table 4.7"

AZE_MACRO_MAIN_PERIODIC_RAW_TABLE = "aze_macro_main_periodic_raw"
AZE_MACRO_MAIN_PERIODIC_TABLE = "aze_macro_main_periodic"
AZE_MACRO_MAIN_PERIODIC_SOURCE_NAME = "CBAR statistical bulletin table 1.1"

AZE_BALANCE_OF_PAYMENTS_PERIODIC_RAW_TABLE = "aze_balance_of_payments_periodic_raw"
AZE_BALANCE_OF_PAYMENTS_PERIODIC_TABLE = "aze_balance_of_payments_periodic"
AZE_BALANCE_OF_PAYMENTS_SOURCE_NAME = "CBAR statistical bulletin table 1.4"

AZE_FOREIGN_TRADE_PERIODIC_RAW_TABLE = "aze_foreign_trade_periodic_raw"
AZE_FOREIGN_TRADE_PERIODIC_TABLE = "aze_foreign_trade_periodic"
AZE_FOREIGN_TRADE_SOURCE_NAME = "CBAR statistical bulletin table 1.5"

AZE_MOVABLE_PROPERTY_REGISTRY_PERIODIC_RAW_TABLE = "aze_movable_property_registry_periodic_raw"
AZE_MOVABLE_PROPERTY_REGISTRY_PERIODIC_TABLE = "aze_movable_property_registry_periodic"
AZE_MOVABLE_PROPERTY_REGISTRY_SOURCE_NAME = "CBAR statistical bulletin table 8"

AZE_NPL_STRUCTURE_PERIODIC_RAW_TABLE = "aze_npl_structure_periodic_raw"
AZE_NPL_STRUCTURE_PERIODIC_TABLE = "aze_npl_structure_periodic"
AZE_NPL_STRUCTURE_SOURCE_NAME = "CBAR statistical bulletin table 5.6"

AZE_INTEREST_RATES_PERIODIC_RAW_TABLE = "aze_interest_rates_periodic_raw"
AZE_INTEREST_RATES_PERIODIC_TABLE = "aze_interest_rates_periodic"
AZE_INTEREST_RATES_SOURCE_NAME = "CBAR statistical bulletin table 3.2"

# Gold marts
AZE_CREDIT_ACCESS_AND_STABILITY_TABLE = "aze_credit_access_and_stability_periodic"
AZE_CREDIT_ACCESS_AND_STABILITY_SOURCE_NAME = "Azerbaijan credit access and stability gold mart"

AZE_DIGITAL_FINANCE_TABLE = "aze_digital_finance_periodic"
AZE_DIGITAL_FINANCE_SOURCE_NAME = "Azerbaijan digital finance gold mart"

AZE_ECONOMIC_DIVERSIFICATION_TABLE = "aze_economic_diversification_periodic"
AZE_ECONOMIC_DIVERSIFICATION_SOURCE_NAME = "Azerbaijan economic diversification gold mart"