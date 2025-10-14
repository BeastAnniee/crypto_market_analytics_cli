
import os
import src.data_ingestion as di
import src.data_cleaning as dc
import src.analysis_models as am
import src.visualizer as vis
import src.utils as utils


# --- Main Menu Functions ---

def handle_web_consults():
    """Handles the 'Consulta web' submenu."""
    utils.print_separator(0)
    print("Web Consult Menu:\n 1. Fetch Top 10 Tickers\n 2. Return to Main Menu")
    option = utils.input_validated_int(1, 2, "Select an option:")
    utils.print_separator(0)

    if option == 1:
        di.fetch_and_save_tickers()
    elif option == 2:
        # NOTE: Full implementation requires user selection, which is complex for a CLI
        print("Market fetching feature is under development. Please use Tickers option.")

    utils.print_separator(1)


def handle_analytics():
    """Handles the 'Statistics' submenu."""

    csv_dir = 'reports/data_raw_exports'
    if not os.path.exists(csv_dir):
        print("You must fetch Tickers data first (Menu 1, Option 1) to perform analysis.")
        return

    # 1. Selección de archivo (Lógica sin cambios)
    print("Select the data file to analyze:")
    available_files = [f for f in os.listdir(csv_dir) if f.endswith('.txt')]
    if not available_files:
        print("No Tickers files found for analysis.")
        return

    for i, file in enumerate(available_files):
        print(f" {i + 1}. {file}")

    file_selection = utils.input_validated_int(1, len(available_files), "Select a file:") - 1
    selected_filename = available_files[file_selection]

    try:
        df = dc.load_data_from_csv(selected_filename)
        if df.empty:
            return
    except FileNotFoundError as e:
        print(e)
        return

    # --- Analytics Submenu Loop ---
    while True:
        utils.print_separator(0)

        print("Analysis Submenu:\n")
        print("--- Basic Models ---\n 1. Predict Future Trend (Min Squares)\n 2. Weighted Average Change\n")
        print(
            "--- Advanced Models ---\n 3. Linear Regression (Scikit-learn)\n 4. Volatility and Risk Analysis\n 5. Best Growth Coin\n")
        print(" 6. Return to Main Menu\n")

        # Validation range updated to [1, 6]
        option = utils.input_validated_int(1, 6, "Select an analysis option:")
        utils.print_separator(0)

        if option == 6:
            break

        # Initialize variables
        selected_coin = None
        result_dict = None
        output_msg = None

        coin_names = df['name'].tolist()

        # Determine if we need to select a currency (Options 1, 2, 3, 4)
        if option in [1, 2, 3, 4]:
            print("Select a coin to analyze:")
            for i, name in enumerate(coin_names):
                print(f" {i + 1}. {name}")
            coin_selection = utils.input_validated_int(1, len(coin_names), "Select a coin:") - 1
            selected_coin = coin_names[coin_selection]

        # Model Execution
        if option == 1:
            result_dict, output_msg = am.min_squares_prediction(df, selected_coin)

        elif option == 2:
            result_dict, output_msg = am.weighted_average_change(df, selected_coin)

        elif option == 3:
            result_dict, output_msg = am.linear_regression_prediction(df, selected_coin)

        elif option == 4:
            result_dict, output_msg = am.calculate_volatility(df, selected_coin)

        elif option == 5:
            # Best Growth Coin no necesita selección de moneda
            result_dict, output_msg = am.get_best_growth_coin(df)

        # Generate Report (Now use dictionary and message)
        # Only runs if results are not empty (search failure, etc.)
        if result_dict and output_msg:
            utils.generate_report_file(selected_filename, result_dict, output_msg)

        utils.print_separator(1)


def handle_visualization():
    """Handles the 'Graficas' submenu."""

    csv_dir = 'reports/data_raw_exports'
    if not os.path.exists(csv_dir):
        print("You must fetch Tickers data first (Menu 1, Option 1) to generate graphs.")
        return

    # --- File Selection Logic ---
    available_files = [f for f in os.listdir(csv_dir) if f.endswith('.txt')]
    if not available_files:
        print("No Tickers files found for visualization.")
        return

    print("Select the data file for visualization:")
    available_files = [f for f in os.listdir(csv_dir) if f.endswith('.txt')]

    for i, file in enumerate(available_files):
        print(f" {i + 1}. {file}")

    file_selection = utils.input_validated_int(1, len(available_files), "Select a file:") - 1
    selected_filename = available_files[file_selection]

    try:
        df = dc.load_data_from_csv(selected_filename)
        if df.empty:
            return
    except FileNotFoundError as e:
        print(e)
        return

    filepath = None
    utils.print_separator(0)
    print("Select the type of visualization:")
    print("--- Basic Charts ---")
    print(" 1. Bar Chart (Change over time)\n")
    print("--- Advanced Analysis Charts ---")
    print(" 2. Regression Scatter Plot (7d Change vs. Price)\n 3. Trend Projection (Line Plot)\n")

    # New validation range: [1, 3]
    option = utils.input_validated_int(1, 3, "Select an option:")

    if option == 1:
        # Submenu for Bar Chart time selection (reusing old logic)
        print("Select time for Bar Chart: 1. 7 days, 2. 24 hours, 3. 1 hour")
        time_option = utils.input_validated_int(1, 3, "Elige una opción: ")

        if time_option == 1:
            filepath = vis.generate_bar_chart(df, 'percent_change_7d', "7 days")
        elif time_option == 2:
            filepath = vis.generate_bar_chart(df, 'percent_change_24h', "24 hours")
        elif time_option == 3:
            filepath = vis.generate_bar_chart(df, 'percent_change_1h', "1 hour")

    elif option == 2:
        # Regression Scatter Plot
        filepath = vis.generate_regression_plot(df)

    elif option == 3:
        # Trend Projection - CURRENCY SELECTION REQUIRED

        coin_names = df['name'].tolist()
        print("\nSelect a coin to project its short-term trend:")
        for i, name in enumerate(coin_names):
            print(f" {i + 1}. {name}")
        coin_selection = utils.input_validated_int(1, len(coin_names), "Select a coin:") - 1
        selected_coin = coin_names[coin_selection]

        filepath = vis.generate_trend_projection_plot(df, selected_coin)

    # Print the save path if a file was generated
    if filepath:
        print(f"Visualization saved to: {filepath}")

    utils.print_separator(1)


def handle_records_consults():
    """
    Handles the 'Records Consults' submenu.
    Allows the user to select a raw data file and view its cleaned Pandas DataFrame.
    """
    csv_dir = 'reports/data_raw_exports'
    if not os.path.exists(csv_dir):
        print("No raw data files found. Please run 'Web Consults' first (Menu 1, Option 1).")
        utils.print_separator(1)
        return

    print("Select the raw data file to view as a clean DataFrame:")
    available_files = [f for f in os.listdir(csv_dir) if f.endswith('.txt') or f.endswith('.csv')]

    if not available_files:
        print("No raw data files found for viewing.")
        utils.print_separator(1)
        return

    for i, file in enumerate(available_files):
        print(f" {i + 1}. {file}")

    try:
        file_selection = utils.input_validated_int(1, len(available_files), "Select a file:") - 1
        selected_filename = available_files[file_selection]
    except ValueError:
        print("Invalid selection.")
        utils.print_separator(1)
        return

    utils.print_separator(0)

    # Load and Clean Data (The core purpose of this option)
    try:
        df = dc.load_data_from_csv(selected_filename)

        if not df.empty:
            print(f"--- Cleaned Data Frame for: {selected_filename} ---")
            # Print only the first few rows for clean console output
            print(df.head())
            print(f"\nDataFrame Shape: {df.shape}")
            print(f"Data Types:\n{df.dtypes}")
        else:
            print(f"DataFrame for {selected_filename} is empty or failed to load.")

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred during loading: {e}")

    utils.print_separator(1)


def main_menu():
    """The main application loop."""
    option = 0
    while option != 6:
        print("\n**Welcome to CMA CLI Tool. Select an option.**\n")
        print(
            "Main Menu Options:\n 1. Web Consults\n 2. Records Consults\n 3. Analytics\n 4. Visualizations\n 5. Delete All Reports\n 6. Exit\n")
        option = utils.input_validated_int(1, 6, "Select an option:")
        utils.print_separator(0)

        if option == 1:
            handle_web_consults()
        elif option == 2:
            # FIX: Call the new function
            handle_records_consults()
        elif option == 3:
            handle_analytics()
        elif option == 4:
            handle_visualization()
        elif option == 5:
            utils.clear_all_reports()
        elif option == 6:
            print("Exiting application. Goodbye!")

        utils.print_separator(1)


if __name__ == "__main__":
    main_menu()