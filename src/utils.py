
import os
#import csv
#import json
#import numpy as np

from src.data_ingestion import ensure_directory_exists

REPORT_OUTPUT_DIR = 'reports/analysis_outputs'


def generate_report_file(doc_name, result_message):
    """
    Writes the analysis result message to a dedicated report file.

    Args:
        doc_name (str): The name of the input data file.
        result_message (str): The formatted message containing the analysis results.
    """
    ensure_directory_exists(REPORT_OUTPUT_DIR)

    # Use the input document name as part of the report name
    report_filename = f"report_{doc_name.replace('.txt', '').replace('consulta_', '')}.txt"
    filepath = os.path.join(REPORT_OUTPUT_DIR, report_filename)

    print(f"\n--- Analysis Result ---\n{result_message}")

    # Append the new report content
    with open(filepath, 'a') as report_file:
        report_file.write(result_message + "\n")

    print(f"\nReport updated successfully in: {filepath}")


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