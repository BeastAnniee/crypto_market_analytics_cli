
import os
import pandas as pd


def load_data_from_csv(filename):
    """
    Loads raw market data from a CSV file into a Pandas DataFrame,
    performing the necessary cleanup and type conversion.

    Args:
        filename (str): The name of the CSV file to load.

    Returns:
        pd.DataFrame: A cleaned DataFrame ready for analysis, or an empty DataFrame on error.
    """
    csv_dir = 'reports/data_raw_exports'
    filepath = os.path.join(csv_dir, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: File not found at {filepath}")

    try:
        # Load the CSV, ignoring the first line of the raw file
        df = pd.read_csv(filepath, sep=',', skiprows=1, header=None)

        # Assign columns based on the structure of the coins.txt file
        df.columns = ['id', 'symbol', 'name', 'nameid', 'rank', 'price_usd',
                      'percent_change_24h', 'percent_change_1h', 'percent_change_7d',
                      'price_btc', 'market_cap_usd', 'volume24', 'volume24a',
                      'csupply', 'tsupply', 'msupply']

        # Convert necessary change columns to numeric (float) for analysis
        numeric_cols = ['percent_change_24h', 'percent_change_1h', 'percent_change_7d']
        for col in numeric_cols:
            # Use .loc for safe assignment
            df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')

        return df

    except Exception as e:
        print(f"Error loading or cleaning the DataFrame: {e}")
        return pd.DataFrame()