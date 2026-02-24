import sys
import os

# Options: 'System', 'Light', 'Dark'
ui_theme = 'System'
# ui_theme = 'Light'
# Options: blue, dark-blue, green, dark-green, purple, dark-purple, orange, dark-orange
color_theme = 'blue'

# Path when running as a normal Python script
assets_path = 'assets'
if hasattr(sys, '_MEIPASS'):
    # Path when running as a compiled PyInstaller executable
    assets_path = os.path.join(sys._MEIPASS, assets_path)

app_icon_name = 'app_icon.ico'
excel_icon_name_light = 'excel_icon_no_bg.png'
excel_icon_name_dark = 'excel_icon_no_bg.png'
folder_icon_name_light = 'folder_icon_no_bg.png'
folder_icon_name_dark = 'folder_icon_no_bg.png'

window_title = 'Stima Impianti'
window_geometry = '800x800'

name_column_header = 'nome'
price_column_header = 'prezzo'

cap_search_results = 15
