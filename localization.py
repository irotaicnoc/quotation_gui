CURRENT_LANG = "en"

TRANSLATIONS = {
    "en": {
        "app_title": "App UI Schema",
        "theme": "Theme:",
        "language": "Language:",
        "system": "System",
        "light": "Light",
        "dark": "Dark",
        "load_config": "Load Configuration",
        "save_data": "Save Data",
        "run_calc": "Run Calculations",
        "add_row": "+ Add Row",
        "browse": "Browse",
        "name": "Name",
        "spec1": "Spec 1",
        "spec2": "Spec 2",
        "price": "Price",
        "quantity": "Quantity",
        "subtotal": "Sub-total",
        "empty": "",
        "industrial_plant": "Industrial Plant",
        "product": "Product",
        "manufacturer": "Manufacturer",
        "confirm": "Confirm",
        "close_prompt": "Close {tab_name}?",
        "error": "Error",
        "could_not_load": "Could not load file:\n",
        "calc_results": "Calculation Results",
        "plant_totals": "Industrial Plant Totals:",
        "grand_total": "Grand Total:",
        "save_dialog": "Save Data",
        "load_dialog": "Load Data"
    },
    "it": {
        "app_title": "Schema UI dell'App",
        "theme": "Tema:",
        "language": "Lingua:",
        "system": "Sistema",
        "light": "Chiaro",
        "dark": "Scuro",
        "load_config": "Carica Configurazione",
        "save_data": "Salva Dati",
        "run_calc": "Esegui Calcoli",
        "add_row": "+ Aggiungi Riga",
        "browse": "Sfoglia",
        "name": "Nome",
        "spec1": "Spec 1",
        "spec2": "Spec 2",
        "price": "Prezzo",
        "quantity": "Quantità",
        "subtotal": "Subtotale",
        "empty": "",
        "industrial_plant": "Impianto Industriale",
        "product": "Prodotto",
        "manufacturer": "Produttore",
        "confirm": "Conferma",
        "close_prompt": "Chiudere {tab_name}?",
        "error": "Errore",
        "could_not_load": "Impossibile caricare il file:\n",
        "calc_results": "Risultati del Calcolo",
        "plant_totals": "Totali Impianto Industriale:",
        "grand_total": "Totale Generale:",
        "save_dialog": "Salva Dati",
        "load_dialog": "Carica Dati"
    }
}


def set_language(lang_code):
    global CURRENT_LANG
    if lang_code in TRANSLATIONS:
        CURRENT_LANG = lang_code


def tr(key):
    return TRANSLATIONS.get(CURRENT_LANG, {}).get(key, key)
