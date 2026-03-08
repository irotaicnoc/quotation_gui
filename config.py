from pathlib import Path


# SETTINGS
CURRENT_LANG = "it"
# CURRENT_LANG = "en"

# possible values:
# - "yes": ask to accept EULA each time the app is started
# - "no": never ask to accept EULA
# - "auto": ask only the first time (stores a flag with the OS)
INITIAL_EULA_DIALOG = "auto"


# LEGAL_INFO
COMPANY_NAME = "MarcoConciatori"
APP_NAME = "StimaImpianti"
APP_VERSION = "0.5.0"
YEAR = 2026


# PATHS
# # Folders
STYLES_FOLDER_PATH = Path("styles")
ASSETS_FOLDER_PATH = Path("assets")
LICENSES_FOLDER_PATH = Path("licenses")
EXCEL_FOLDER_PATH = Path(".")

# # Files
APP_ICON_NAME = "app_icon.ico"
EXCEL_ICON_NAME = "excel_icon_no_bg.png"

GENERIC_CUSTOM_STYLE_NAME = "style.qss"
MENU_CUSTOM_STYLE_NAME = "menu_style.qss"
TAB_CUSTOM_STYLE_NAME = "tab_style.qss"

LICENSE_FILE_NAME = "EULA.txt"
THIRD_PARTY_LICENSE_FILE_NAME = "THIRDPARTY_LICENSES.json"
PRODUCT_FILES = {
    "product_1": "INTERFACCIA-2025-sez01.2.xlsx",
    "product_2": "another_file.xlsx",
}
