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

TRADE_TARGETS = [
    {"reporter_iso3": "GHA", "reporter_name": "Ghana",      "hs_code": "0901", "hs_label": "Coffee",      "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "GHA", "reporter_name": "Ghana",      "hs_code": "1801", "hs_label": "Cocoa beans", "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "BRA", "reporter_name": "Brazil",     "hs_code": "0901", "hs_label": "Coffee",      "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "BRA", "reporter_name": "Brazil",     "hs_code": "1801", "hs_label": "Cocoa beans", "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "AZE", "reporter_name": "Azerbaijan", "hs_code": "2709", "hs_label": "oils",        "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "BRA", "reporter_name": "Brazil",     "hs_code": "7113", "hs_label": "Jewellery",   "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "KAZ", "reporter_name": "Kazakhstan", "hs_code": "7113", "hs_label": "Jewellery",   "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "JPN", "reporter_name": "Japan",      "hs_code": "7113", "hs_label": "Jewellery",   "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "JPN", "reporter_name": "Japan",      "hs_code": "2709", "hs_label": "oils",        "flow_code": "M", "flow_name": "Import"}

]

TRADE_PARTNER_CODE = "0"
TRADE_PARTNER_NAME = "World"

TRADE_START_YEAR = 2004
TRADE_END_YEAR = 2023

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