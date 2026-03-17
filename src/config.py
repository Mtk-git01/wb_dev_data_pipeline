PROJECT_ID = "worldbank01"
DATASET_ID = "wb_dev_stats"

U5MR_TABLE_ID = "u5mr_country_year"
U5MR_URL = "https://childmortality.org/wp-content/uploads/2024/03/UNIGME-2024-Total-U5MR-IMR-and-NMR-database.xlsx"

GIRLS_PRIMARY_COMPLETION_TABLE_COUNTRY_YEAR = "girls_primary_completion_country_year"
GIRLS_PRIMARY_COMPLETION_TABLE_COUNTRY_LATEST = "girls_primary_completion_country_latest"
WB_API_BASE = "https://api.worldbank.org/v2"
GIRLS_PRIMARY_COMPLETION_INDICATOR_CODE = "SE.PRM.CMPT.FE.ZS"
GIRLS_PRIMARY_COMPLETION_INDICATOR_NAME = "Primary completion rate, female (% of relevant age group)"
GIRLS_PRIMARY_COMPLETION_SOURCE_NAME = "World Bank API"


TRADE_TABLE_COUNTRY_YEAR = "trade_country_year_long"
TRADE_TABLE_COUNTRY_LATEST = "trade_country_latest"

TRADE_SOURCE_NAME = "UN Comtrade"

TRADE_TARGETS = [
    {"reporter_iso3": "GHA", "reporter_name": "Ghana",      "hs_code": "0901", "hs_label": "Coffee",      "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "GHA", "reporter_name": "Ghana",      "hs_code": "1801", "hs_label": "Cocoa beans", "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "BRA", "reporter_name": "Brazil",     "hs_code": "0901", "hs_label": "Coffee",      "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "BRA", "reporter_name": "Brazil",     "hs_code": "1801", "hs_label": "Cocoa beans", "flow_code": "X", "flow_name": "Export"},
    {"reporter_iso3": "BRA", "reporter_name": "Brazil",     "hs_code": "7113", "hs_label": "Jewellery",   "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "KAZ", "reporter_name": "Kazakhstan", "hs_code": "7113", "hs_label": "Jewellery",   "flow_code": "M", "flow_name": "Import"},
    {"reporter_iso3": "JPN", "reporter_name": "Japan",      "hs_code": "7113", "hs_label": "Jewellery",   "flow_code": "M", "flow_name": "Import"},
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
}