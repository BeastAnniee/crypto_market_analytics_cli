
import os
import json
from datetime import datetime

from src.data_ingestion import ensure_directory_exists

REPORT_OUTPUT_DIR = 'reports/analysis_outputs'


def generate_report_file(doc_name, analysis_results_dict, output_message):
    """
    Saves the analysis results (dict) to a JSON file and displays the message.

    Args:
        doc_name (str): The input file name for reference.
        analysis_results_dict (dict): The Python dictionary with the numerical results.
        output_message (str): The user-friendly message for the console.
    """
    ensure_directory_exists(REPORT_OUTPUT_DIR)

    # Prepare the JSON filename (without timestamp to consolidate reports)
    report_filename = f"analysis_report_{doc_name.replace('.txt', '').replace('consulta_', '')}.json"
    filepath = os.path.join(REPORT_OUTPUT_DIR, report_filename)

    # Add metadata
    analysis_results_dict['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Read/Write Logic for Stacking JSON Results ---
    data = []

    # Attempt to read existing data
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            # Empty or corrupt file, we will overwrite it
            pass

    # Add the new result
    data.append(analysis_results_dict)

    # Write the complete array back
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)  # We use indent=4 for readable formatting

    print(f"\n--- Analysis Result ---\n{output_message}")
    print(f"Structured results saved successfully to: {filepath}")

def input_validated_int(min_val, max_val, prompt=""):
    """
    Ensures user input is an integer within a specified range [min_val, max_val].

    Returns:
        int: The validated user input.
    """
    while True:
        try:
            print(prompt)
            lect = int(input("-----> "))

            if min_val <= lect <= max_val:
                print("")
                return lect
            else:
                print(f"Invalid input. Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")



def print_separator(n):
    """Prints a standardized separator for cleaner console output."""
    if n == 0:
        print("\n--------------------------------------\n")
    else:
        print("\n=======================================\n")


def clear_all_reports():
    """Deletes all generated reports and directories."""
    import shutil

    dirs_to_delete = [
        'reports',
        'Graficas',  # If you had a legacy folder
    ]

    print("Deleting all generated reports and directories...")

    for directory in dirs_to_delete:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
                print(f"Directory '{directory}' deleted successfully.")
            except OSError as e:
                print(f"Error deleting directory '{directory}': {e}")
        else:
            print(f"Directory '{directory}' does not exist.")

    print("All generated files have been eliminated.")