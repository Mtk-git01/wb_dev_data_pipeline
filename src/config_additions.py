# ==============================
# Additional datasets
# Append these constants to src/config.py
# ==============================

RAW_DATA_DIR = "data/raw"

# ------------------------------
# Global Findex
# ------------------------------
GLOBAL_FINDEX_TABLE_COUNTRY_YEAR = "global_findex_country_year"
GLOBAL_FINDEX_TABLE_COUNTRY_LATEST = "global_findex_country_latest"
GLOBAL_FINDEX_SOURCE_NAME = "World Bank Global Findex"
# Recommended: manually download official country-level CSV/XLSX and place under data/raw/
GLOBAL_FINDEX_INPUT_PATH = f"{RAW_DATA_DIR}/global_findex_country.csv"
GLOBAL_FINDEX_SERIES_MAP = {
    "account_ownership_pct": [
        "Account ownership at a financial institution or with a mobile-money-service provider (% age 15+)",
        "Account ownership at a financial institution or with a mobile money provider (% age 15+)"
    ],
    "digital_payment_pct": [
        "Made or received digital payments in the past year (% age 15+)",
    ],
    "formal_borrowing_pct": [
        "Borrowed from a financial institution in the past year (% age 15+)",
    ],
    "saved_financial_institution_pct": [
        "Saved at a financial institution in the past year (% age 15+)",
    ],
    "female_account_ownership_pct": [
        "Account ownership, female (% age 15+)",
    ],
    "male_account_ownership_pct": [
        "Account ownership, male (% age 15+)",
    ],
}

# ------------------------------
# IMF Financial Access Survey
# ------------------------------
IMF_FAS_TABLE_COUNTRY_YEAR = "imf_fas_country_year"
IMF_FAS_TABLE_COUNTRY_LATEST = "imf_fas_country_latest"
IMF_FAS_SOURCE_NAME = "IMF Financial Access Survey"
# Recommended: download official CSV extract and place under data/raw/
IMF_FAS_INPUT_PATH = f"{RAW_DATA_DIR}/imf_fas.csv"
IMF_FAS_SERIES_MAP = {
    "commercial_bank_branches_per_100k": [
        "Commercial bank branches per 100,000 adults",
    ],
    "atms_per_100k": [
        "ATMs per 100,000 adults",
    ],
    "deposit_accounts_per_1000": [
        "Deposit accounts with commercial banks per 1,000 adults",
    ],
    "borrowers_per_1000": [
        "Borrowers from commercial banks per 1,000 adults",
    ],
    "outstanding_loans_private_sector_pct_gdp": [
        "Outstanding loans from commercial banks (% of GDP)",
        "Outstanding loans from commercial banks to the private sector (% of GDP)",
    ],
}

# ------------------------------
# Worldwide Governance Indicators
# ------------------------------
WGI_TABLE_COUNTRY_YEAR = "wgi_country_year"
WGI_TABLE_COUNTRY_LATEST = "wgi_country_latest"
WGI_SOURCE_NAME = "Worldwide Governance Indicators"
# Recommended: download official bulk CSV/XLSX and place under data/raw/
WGI_INPUT_PATH = f"{RAW_DATA_DIR}/wgi.xlsx"
WGI_SERIES_MAP = {
    "voice_accountability": ["Voice and Accountability: Estimate"],
    "political_stability": ["Political Stability and Absence of Violence/Terrorism: Estimate"],
    "government_effectiveness": ["Government Effectiveness: Estimate"],
    "regulatory_quality": ["Regulatory Quality: Estimate"],
    "rule_of_law": ["Rule of Law: Estimate"],
    "control_of_corruption": ["Control of Corruption: Estimate"],
}
