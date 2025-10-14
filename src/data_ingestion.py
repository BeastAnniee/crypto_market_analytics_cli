
import requests
import json
import csv
import os
import datetime
#import pandas as pd

# Define the base directory for raw data exports
REPORTS_DIR = 'reports/data_raw_exports'
TICKERS_FIELDNAMES = ['id', 'symbol', 'name', 'nameid', 'rank', 'price_usd',
                      'percent_change_24h', 'percent_change_1h', 'percent_change_7d',
                      'price_btc', 'market_cap_usd', 'volume24', 'volume24a',
                      'csupply', 'tsupply', 'msupply']


def ensure_directory_exists(path):
    """Creates the specified directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def save_data_to_csv(data, filename_prefix, fieldnames):
    """
    Saves a list of dictionaries to a CSV file in the raw exports' directory.

    Returns the full path of the saved file.
    """
    ensure_directory_exists(REPORTS_DIR)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = os.path.join(REPORTS_DIR, f"{filename_prefix}_{timestamp}.txt")

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

    return filepath


def fetch_and_save_tickers():
    """Fetches the top 10 tickers from the API and saves the raw data."""
    API_URL = "https://api.coinlore.net/api/tickers/?start=0&limit=10"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        content_data = json.loads(response.content)
        data = content_data.get("data", [])

        if data:
            filepath = save_data_to_csv(
                data=data,
                filename_prefix="consulta_tickers",
                fieldnames=TICKERS_FIELDNAMES
            )
            print(f"Ticker data successfully saved to: {filepath}")
            return filepath
        else:
            print("Error: API returned no data.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        return None


def fetch_and_save_markets():
    print("Market fetch logic needs a coin ID. Check main menu flow.")
    return None