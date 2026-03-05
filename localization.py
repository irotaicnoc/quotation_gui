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
        "could_not_load": "Could not load file:",
        "calc_results": "Calculation Results",
        "plant_totals": "Industrial Plant Totals:",
        "grand_total": "Grand Total:",
        "save_dialog": "Save Data",
        "load_dialog": "Load Data",
        "select_products": "Select Products",
        "cancel": "Cancel",
        "select": "Select",
        "error_loading_file": "Error loading file",
        "eula_title": "End User License Agreement",
        "eula_accept_label": "Please read and accept the EULA to continue:",
        "file_not_found_error": "Error: {file_name} not found.",
        "close": "Close",
        "accept": "Accept",
        "decline": "Decline",
        "about_title": "About",
        "about_text": "<b>{app_name} v{app_version}</b><br>© {year} {company_name}. All rights reserved."
                      "<br><br><i>Third-party credits (and their dependencies):</i><br>",
        "view_eula": "View EULA",
        "view_third_party": "Third-Party Licenses",
        "third_party_error": "Error: {file_name} not found.",
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
        "could_not_load": "Impossibile caricare il file:",
        "calc_results": "Risultati del Calcolo",
        "plant_totals": "Totali Impianto Industriale:",
        "grand_total": "Totale Generale:",
        "save_dialog": "Salva Dati",
        "load_dialog": "Carica Dati",
        "select_products": "Seleziona Prodotti",
        "cancel": "Annulla",
        "select": "Seleziona",
        "error_loading_file": "Errore nel caricamento del file",
        "eula_title": "Accordo di Licenza per l'Utente Finale",
        "eula_accept_label": "Si prega di leggere e accettare l'EULA per continuare:",
        "file_not_found_error": "Errore: {file_name} non trovato.",
        "close": "Chiudi",
        "accept": "Accetta",
        "decline": "Rifiuta",
        "about_title": "Informazioni",
        "about_text": "<b>{app_name} v{app_version}</b><br>© {year} {company_name}. Tutti i diritti riservati."
                      "<br><br><i>Crediti di terze parti (e relative dipendenze):</i><br>",
        "view_eula": "Visualizza EULA",
        "view_third_party": "Licenze di Terze Parti",
        "third_party_error": "Errore: {file_name} non trovato.",
    }
}


def set_language(lang_code):
    if lang_code in TRANSLATIONS:
        config.CURRENT_LANG = lang_code


def translate(key, **kwargs):
    text = TRANSLATIONS.get(config.CURRENT_LANG, {}).get(key, key)

    if kwargs:
        # This automatically replaces {key} with the provided value
        return text.format(**kwargs)

    return text
