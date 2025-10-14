# Crypto Market Analytics (CMA) CLI Tool
## Overview
CMA is a Quantitative Data Analysis and ETL (Extract, Transform, Load) Tool built entirely in Python. This project demonstrates a complete scientific programming workflow: from data ingestion and cleaning to applying numerical models and generating visualizations.

The goal is to provide fast, data-driven insights into cryptocurrency market trends using a simple Command-Line Interface (CLI).
_____

## Key Features

| Feature | Description |
| :--- | :--- |
| **Data Ingestion Pipeline** | Uses the `requests` library to fetch top-tier ticker data from a public API, storing raw output in a structured file system. |
| **Advanced Quantitative Modeling** | Implements numerical methods like **Least Squares Regression** for short-term trend prediction and **Linear Regression** using **scikit-learn** to analyze correlations between 7-day and 24-hour changes. |
| **Data Cleaning** | Uses the **Pandas** library to load raw files, perform necessary data type conversions, and prepare the data for analysis. |
| **Modular Architecture** | Project logic is split into dedicated modules (`analysis_models`, `data_ingestion`, `visualizer`) for high maintainability and testability. |
| **Advanced Visualization** | Generates insightful charts using **Matplotlib** and **Seaborn**: bar charts for percentage changes, scatter plots with regression lines, and trend projection line plots. |
| **Structured JSON Reports** | Analysis results are saved as structured JSON files with timestamps, enabling historical tracking and data serialization. |

## Project Architecture
The project is structured following professional Python standards, separating core responsibilities into distinct modules:
```powershell
.
├── src/
│   ├── analysis_models.py
│   ├── data_cleaning.py
│   ├── data_ingestion.py
│   ├── visualizer.py
│   ├── utils.py
│   └── main.py
├── reports/
│   ├── analysis_outputs/
│   ├── data_raw_exports/
│   └── visualizations/
└── tests/
```

## Getting Started
### Prerequisites
- Python 3.x

### Installation
Clone the repository:
```powershell
git clone https://github.com/BeastAnniee/crypto_market_analytics_cli
cd crypto_market_analytics_cli
```
Create a virtual environment (Recommended):
```powershell
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```
Install dependencies:
(Based on your requirements.txt)
```powershell
pip install -r requirements.txt
```
### Running the Application
Execute the main file from the project root:
```powershell
python3 src/main.py
```
## Usage Flow
The application runs via the CLI, guiding the user through the following process:

Menu 1: Web Consults → Fetches top 10 tickers and saves the raw data (Input for the pipeline).

Menu 3: Analytics → Selects a saved file, cleans it, and applies the numerical models (e.g., Least Squares) to predict trends.

Menu 4: Visualizations → Selects a saved file and generates a Matplotlib bar chart for the selected time change.