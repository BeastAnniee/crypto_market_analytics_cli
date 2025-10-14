
import os
import matplotlib.pyplot as plt
import seaborn as sns # Seaborn for better box plots
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression # Needed for plotting the line

VISUALIZATIONS_DIR = 'reports/visualizations'

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


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


def generate_regression_plot(df):
    """
    Generates a scatter plot showing the relationship between 7-day change (X)
    and 24-hour change (Y), with the Linear Regression line superimposed.
    """
    ensure_directory_exists(VISUALIZATIONS_DIR)

    # 1. Defining Columns for Logistic Regression
    x_column = 'percent_change_7d'
    y_column = 'percent_change_24h'

    # 2. Fit the model to get the line parameters
    X = df[x_column].values.reshape(-1, 1)
    y = df[y_column].values
    model = LinearRegression()
    model.fit(X, y)

    # Generate the unique filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Graph_Regression_{x_column}_vs_{y_column}_{timestamp}.png"
    filepath = os.path.join(VISUALIZATIONS_DIR, filename)

    # --- Matplotlib/Seaborn Generation ---
    plt.figure(figsize=(10, 6))

    # Plot the scatter points
    sns.scatterplot(x=x_column, y=y_column, data=df, label='Data Points')

    # Plot the regression line
    plt.plot(df[x_column], model.predict(X), color='red',
             label=f'Regression Line (Slope: {model.coef_[0]:.2f})')

    plt.xlabel('7-Day Percentage Change (%)')
    plt.ylabel('24-Hour Percentage Change (%)')
    plt.title('Predictive Relationship: 7-Day vs. 24-Hour Change')

    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    plt.savefig(filepath)
    plt.close()

    return filepath


def generate_trend_projection_plot(df, coin_name):
    """
    Generates a line plot showing the short-term trend projection
    using the three percentage change points (1h, 24h, 7d).

    Args:
        df (pd.DataFrame): The cleaned DataFrame.
        coin_name (str): The specific coin to plot.

    Returns: The filepath of the saved image.
    """
    ensure_directory_exists(VISUALIZATIONS_DIR)

    # 1. Extract the change data
    coin_data = df[df['name'] == coin_name].iloc[0]

    # Percentage change points (Y)
    y_values = coin_data[['percent_change_1h', 'percent_change_24h', 'percent_change_7d']].values

    # Simulated "time" points for visualization (X)
    # We use 1, 24, 168 hours (simulating a time series)
    x_hours = np.array([1, 24, 168])

    # Generate the unique filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Graph_Projection_{coin_name}_{timestamp}.png"
    filepath = os.path.join(VISUALIZATIONS_DIR, filename)

    # --- Matplotlib Generation ---
    plt.figure(figsize=(10, 6))

    # Plot the actual data points
    plt.plot(x_hours, y_values, 'o', color='blue', label='Reported Changes')

    # Generate the Least Squares Trendline (for context)
    # Although the regression was performed with simulated points, here we use it to show the "fit"

    # We will use the original Least Squares data for the fit line (0, 6.85, 7)
    # For simplicity and to avoid recalculating, we will plot a line that goes from point 1h to point 7d

    # Points for the simple trend line (with the last change as projection)
    # To be strict, you would need to calculate the regression line again.
    # We will use a simple line to connect the beginning and the end of the period.

    # --- Fit Line Generation (Adapting Least Squares) ---
    # To get the line, we need the slope (m) and the intercept (b)

    # Points for the fit (we will use only the last point and point 1h for the visual trend)
    X_fit = x_hours.reshape(-1, 1)
    y_fit = y_values

    model = LinearRegression()
    model.fit(X_fit, y_fit)
    y_pred = model.predict(X_fit)

    # Draw the trend line using the model prediction
    plt.plot(x_hours, y_pred, color='red', linestyle='--', label='Linear Trend Line')

    plt.xlabel('Time (Hours)')
    plt.ylabel('Percent Change (%)')
    plt.title(f'Short-Term Change and Trend for {coin_name}')

    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    plt.savefig(filepath)
    plt.close()

    return filepath
