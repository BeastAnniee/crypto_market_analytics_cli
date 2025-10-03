
import numpy as np
import pandas as pd


def min_squares_prediction(df, coin_name):
    """
    Applies the Least Squares method to predict short-term trend
    based on 1h, 24h, and 7d percent changes. Validates NumPy usage.

    Args:
        df (pd.DataFrame): The cleaned DataFrame containing market data.
        coin_name (str): The name of the cryptocurrency to analyze.

    Returns:
        str: A message indicating the predicted trend.
    """
    coin_data = df[df['name'] == coin_name]
    if coin_data.empty:
        return f"Error: Coin '{coin_name}' not found for analysis."

    # Extracting the three percent changes as the dependent variable (Y)
    l = coin_data[['percent_change_1h', 'percent_change_24h', 'percent_change_7d']].values.flatten()

    # Abscissas (X) are defined for the trend calculation based on the original logic
    x = np.array((0, 6.85, 7))

    # Least Squares calculation for the slope (m)
    s_x = np.sum(x)
    s_l = np.sum(l)
    s_xy = np.sum(x * l)
    s_x_sqr = np.sum(x ** 2)

    # Slope formula
    m = (s_xy - (s_x * s_l) / 3) / (s_x_sqr - (s_x ** 2) / 3)

    if m < 0:
        return f"Prediction for {coin_name}: Expected value to decrease (Slope: {m:.4f})"
    elif m == 0:
        return f"Prediction for {coin_name}: Future trend is uncertain (Slope: {m:.4f})"
    else:
        return f"Prediction for {coin_name}: Expected value to increase (Slope: {m:.4f})"


def weighted_average_change(df, coin_name):
    """
    Calculates the weighted average percent change over the last week.
    (More weight on recent changes).

    Args:
        df (pd.DataFrame): The cleaned DataFrame.
        coin_name (str): The name of the cryptocurrency to analyze.

    Returns:
        str: A formatted string with the weighted average.
    """
    coin_data = df[df['name'] == coin_name]
    if coin_data.empty:
        return f"Error: Coin '{coin_name}' not found."

    # Weights: 1h(0.5), 24h(0.33), 7d(0.16)
    wt = np.array([0.5, 0.333333, 0.1666666])

    # Values array (must match weight order)
    values = coin_data[['percent_change_1h', 'percent_change_24h', 'percent_change_7d']].values.flatten()

    avg = np.average(values, weights=wt)
    return f"The weighted average change for {coin_name} (last week) is: {avg:.4f}%"


def get_best_growth_coin(df):
    """Identifies the coin with the best growth based on the weighted average."""

    # Calculate the weighted average for all coins using a helper function
    def calculate_weighted_avg(row):
        wt = np.array([0.5, 0.333333, 0.1666666])
        values = row[['percent_change_1h', 'percent_change_24h', 'percent_change_7d']].values
        return np.average(values, weights=wt)

    df['weighted_avg'] = df.apply(calculate_weighted_avg, axis=1)

    # Find the maximum
    best_coin = df.loc[df['weighted_avg'].idxmax()]

    return f"The coin with the best weighted growth rate is {best_coin['name']} at {best_coin['weighted_avg']:.4f}%"