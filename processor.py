import pandas as pd

import config


def extract_data_from_file(file_path):
    """
    Reads the Excel file and extracts a dictionary mapping 'name' to 'price'.
    """
    try:
        df = pd.read_excel(file_path)
        df.columns = [str(c).lower().strip() for c in df.columns]

        if config.name_column_header in df.columns and config.price_column_header in df.columns:
            # Drop rows where either name or price is missing
            df = df.dropna(subset=[config.name_column_header, config.price_column_header])

            return dict(zip(df[config.name_column_header].astype(str), df[config.price_column_header]))
        else:
            return {}

    except Exception as e:
        print(f'Failed to read {file_path}: {e}')
        return {}


def run_pipeline(totals):
    """
    Receives a list of calculated totals from the UI.
    Returns a formatted string containing the grand total.
    """
    grand_total = sum(totals)

    results = [
        # f'Summing {len(totals)} rows...\n',
        # '-' * 30 + '\n',
        f'Total: {grand_total:.2f}\n',
        '-' * 30 + '\n',
        '✅ Processing complete!'
    ]

    return ''.join(results)
