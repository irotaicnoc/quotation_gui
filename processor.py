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