
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

    # 1. Select the data file
    print("Select the data file to analyze:")
    available_files = [f for f in os.listdir(csv_dir) if f.endswith('.txt')]
    if not available_files:
        print("No Tickers files found for analysis.")
        return

    for i, file in enumerate(available_files):
        print(f" {i + 1}. {file}")

    file_selection = utils.input_validated_int(1, len(available_files), "Select a file:") - 1
    selected_filename = available_files[file_selection]

    # 2. Load and Clean Data (Uses Pandas)
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
        print(
            "Analysis Submenu:\n 1. Predict Future Trend (Min Squares)\n 2. Weighted Average Change\n 3. Best Growth Coin\n 4. Return to Main Menu")
        option = utils.input_validated_int(1, 4, "Select an analysis option:")
        utils.print_separator(0)

        if option == 4:
            break

        selected_coin = None
        result = None

        # Get coin name for options 1 and 2
        coin_names = df['name'].tolist()
        if option in [1, 2]:
            print("Select a coin to analyze:")
            for i, name in enumerate(coin_names):
                print(f" {i + 1}. {name}")
            coin_selection = utils.input_validated_int(1, len(coin_names), "Select a coin:") - 1
            selected_coin = coin_names[coin_selection]

        # Run analysis model
        if option == 1:
            result = am.min_squares_prediction(df, selected_coin)
        elif option == 2:
            result = am.weighted_average_change(df, selected_coin)
        elif option == 3:
            result = am.get_best_growth_coin(df)

        utils.generate_report_file(selected_filename, result)
        utils.print_separator(1)


def handle_visualization():
    """Handles the 'Graficas' submenu."""

    csv_dir = 'reports/data_raw_exports'
    if not os.path.exists(csv_dir):
        print("You must fetch Tickers data first (Menu 1, Option 1) to generate graphs.")
        return

    print("Select the data file for visualization:")
    available_files = [f for f in os.listdir(csv_dir) if f.endswith('.txt')]
    if not available_files:
        print("No Tickers files found for visualization.")
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

    filepath = None

    utils.print_separator(0)
    print("Select the change to visualize:")
    print(" 1. Changes in 7 days\n 2. Changes in 24 hours\n 3. Changes in 1 hour")
    time_option = utils.input_validated_int(1, 3, "Select an option:")

    if time_option == 1:
        filepath = vis.generate_bar_chart(df, 'percent_change_7d', "7 days")
    elif time_option == 2:
        filepath = vis.generate_bar_chart(df, 'percent_change_24h', "24 hours")
    elif time_option == 3:
        filepath = vis.generate_bar_chart(df, 'percent_change_1h', "1 hour")

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