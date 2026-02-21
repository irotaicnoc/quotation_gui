import pandas as pd

import config


def extract_names_from_file(file_path):
    """
    Reads the Excel file and extracts the 'name' column as a list of strings.
    """
    try:
        df = pd.read_excel(file_path)

        # Standardize column headers to lowercase to avoid case-sensitivity bugs
        # (e.g., catching "Name", "NAME", or "name ")
        df.columns = [str(c).lower().strip() for c in df.columns]

        if config.name_column_header in df.columns:
            # Drop empty rows and convert everything to a clean list of strings
            return df[config.name_column_header].dropna().astype(str).tolist()
        else:
            return []

    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
        return []


def run_pipeline(extracted_data):
    """
    Core logic.
    Receives a list of tuples: (target_file, val1, val2)
    Returns a formatted string containing the results to be printed in the UI.
    """
    results = []

    # 1. Setup / Validation
    results.append(f"Starting pipeline with {len(extracted_data)} parameter sets...\n")
    results.append("-" * 30 + "\n")

    # 2. The actual crunching
    for target_file, val1, val2 in extracted_data:
        # NOTE: This is where you will eventually put:
        # df = pd.read_excel(target_file)

        # Placeholder calculation
        calculated_value = val1 * val2

        results.append(f"Target: {target_file}")
        results.append(f"Multiplier Output: {calculated_value}\n")

    results.append("-" * 30 + "\n")
    results.append("✅ Processing complete!")

    # Return the final text block to the UI
    return "".join(results)