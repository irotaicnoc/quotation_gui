CURRENT_LANG = "it"

TRANSLATIONS = {
    "en": {
        "app_title": "Quotation Application",
        "theme": "Theme:",
        "language": "Language:",
        "system": "System",
        "light": "Light",
        "dark": "Dark",
        "load_config": "Load Configuration",
        "save_data": "Save Data",
        "run_calc": "Run Calculations",
        "add_row": "+ Add Row",
        "browse": "Load Excel",
        "name": "Name",
        "description": "Description",
        "part_number": "Part Number",
        "dimension": "Dimension",
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
        "load_dialog": "Load Data",
        "select_products": "Select Products",
        "ok": "OK",
        "cancel": "Cancel",
        "select": "Select",
        "error_loading_file": "Error loading file"
    },
    "it": {
        "app_title": "Programma di Quotazione",
        "theme": "Tema:",
        "language": "Lingua:",
        "system": "Sistema",
        "light": "Chiaro",
        "dark": "Scuro",
        "load_config": "Carica Configurazione",
        "save_data": "Salva Dati",
        "run_calc": "Esegui Calcoli",
        "add_row": "+ Aggiungi Riga",
        "browse": "Lista della Spesa",
        "name": "Nome",
        "description": "Descrizione",
        "part_number": "Codice",
        "dimension": "Dimensione",
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
        "load_dialog": "Carica Dati",
        "select_products": "Seleziona Prodotti",
        "ok": "OK",
        "cancel": "Annulla",
        "select": "Seleziona",
        "error_loading_file": "Errore nel caricamento del file"
    }
}


def set_language(lang_code):
    global CURRENT_LANG
    if lang_code in TRANSLATIONS:
        CURRENT_LANG = lang_code


def translate(key):
    return TRANSLATIONS.get(CURRENT_LANG, {}).get(key, key)
