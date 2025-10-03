
import os
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd


def generate_bar_chart(df, change_column, time_label):
    """
    Generates a bar chart visualizing cryptocurrency percentage changes.

    Args:
        df (pd.DataFrame): The cleaned DataFrame.
        change_column (str): The column name to plot (e.g., 'percent_change_7d').
        time_label (str): The human-readable label for the time period (e.g., '7 days').

    Returns:
        str: The filepath of the saved image.
    """

    VISUALIZATIONS_DIR = 'reports/visualizations'
    if not os.path.exists(VISUALIZATIONS_DIR):
        os.makedirs(VISUALIZATIONS_DIR)

    # Prepare data directly from the DataFrame
    nombres = df['name']
    cambios = df[change_column]

    # Generate the unique filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Graph_Changes_{change_column}_{timestamp}.png"
    filepath = os.path.join(VISUALIZATIONS_DIR, filename)

    # --- Matplotlib Generation ---
    plt.figure(figsize=(10, 5))
    plt.bar(nombres, cambios)

    plt.xlabel('Coin')
    plt.ylabel(f'Change % in {time_label}')
    plt.title(f'Change % in {time_label} for Each Coin')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig(filepath)
    plt.close()  # Close the figure to free memory

    return filepath