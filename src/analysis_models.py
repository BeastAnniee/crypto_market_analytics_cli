
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


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
        trend = "Decrease"
        output_msg = f"Prediction for {coin_name}: Expected value to decrease (Slope: {m:.4f})"
    elif m == 0:
        trend = "Uncertain"
        output_msg = f"Prediction for {coin_name}: Future trend is uncertain (Slope: {m:.4f})"
    else:
        trend = "Increase"
        output_msg = f"Prediction for {coin_name}: Expected value to increase (Slope: {m:.4f})"

    results_dict = {
        'analysis_type': 'Min_Squares_Prediction',
        'coin_analyzed': coin_name,
        'slope': round(m, 4),
        'predicted_trend': trend
    }

    return results_dict, output_msg


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
    if coin_data.empty: return {}, f"Error: Coin '{coin_name}' not found."

    wt = np.array([0.5, 0.333333, 0.1666666])
    values = coin_data[['percent_change_1h', 'percent_change_24h', 'percent_change_7d']].values.flatten()
    avg = np.average(values, weights=wt)

    results_dict = {
        'analysis_type': 'Weighted Average Change',
        'coin_analyzed': coin_name,
        'average_change': round(avg, 4)
    }

    output_msg = f"The weighted average change for {coin_name} (last week) is: {avg:.4f}%"

    return results_dict, output_msg


def get_best_growth_coin(df):
    """Identifies the coin with the best growth based on the weighted average."""

    # Calculate the weighted average for all coins using a helper function
    def calculate_weighted_avg(row):
        wt = np.array([0.5, 0.333333, 0.1666666])
        values = row[['percent_change_1h', 'percent_change_24h', 'percent_change_7d']].values
        return np.average(values, weights=wt)

    df['weighted_avg'] = df.apply(calculate_weighted_avg, axis=1)

    best_coin = df.loc[df['weighted_avg'].idxmax()]

    results_dict = {
        'analysis_type': 'Best Growth Coin',
        'coin_name': best_coin['name'],
        'weighted_avg': round(best_coin['weighted_avg'], 4)
    }

    output_msg = f"The coin with the best weighted growth rate is {best_coin['name']} with {best_coin['weighted_avg']:.4f}%"

    return results_dict, output_msg

def linear_regression_prediction(df, coin_name):
    """
    Applies Linear Regression (Scikit-learn) using 7d change to predict USD price.

    Args:
        df (pd.DataFrame): The cleaned DataFrame.
        coin_name (str): The name of the cryptocurrency to predict.

    Returns:
        dict: Results including R2 score and a simple price prediction.
    """
    # Prepare data (we use all points for the model)
    # X (Feature): 7-day change, Y (Target): USD Price
    X = df['percent_change_7d'].values.reshape(-1, 1)
    y = df['price_usd'].values

    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Evaluate the model
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    # Predict a new simple value (We use the 7d value of the selected currency)
    coin_7d_change = df[df['name'] == coin_name]['percent_change_7d'].values[0]

    # The prediction is simple: if the trend continues, what would be the price?
    predicted_price = model.predict(np.array([[coin_7d_change]]))[0]

    result = {
        'model_name': 'Linear Regression (7d change vs USD price)',
        'coin_analyzed': coin_name,
        'r2_score': round(r2, 4),
        'predicted_price_usd': round(predicted_price, 2)
    }

    output_msg = (
        f"--- ADVANCED ANALYSIS: Linear Regression ---\n"
        f"Model R² Score (Fit Quality): {r2:.4f}\n"
        f"Prediction for {coin_name} (based on its 7d change):\n"
        f"Predicted USD Price: ${predicted_price:.2f}"
    )

    return result, output_msg

def calculate_volatility(df, coin_name):
    """
    Calculates the standard deviation (volatility) of price changes
    over the last 7 days.

    Args:
        df (pd.DataFrame): The cleaned DataFrame.
        coin_name (str): The name of the cryptocurrency.

    Returns:
        dict: Volatility statistics.
    """
    coin_data = df[df['name'] == coin_name]
    if coin_data.empty:
        return None, f"Error: Coin '{coin_name}' not found for volatility analysis."

    # We use the three change points as a proxy for recent volatility
    changes = coin_data[['percent_change_1h', 'percent_change_24h', 'percent_change_7d']].values.flatten()

    std_dev = np.std(changes)

    if std_dev > 5:
        risk = "HIGH"
    elif std_dev > 1:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    result = {
        'coin': coin_name,
        'volatility_std': std_dev,
        'risk_level': risk
    }

    output_msg = (
        f"--- ADVANCED ANALYSIS: Volatility Check ---\n"
        f"Standard Deviation (Volatility) of Recent Changes: {std_dev:.4f}\n"
        f"Calculated Risk Level: {risk}"
    )
    return result, output_msg