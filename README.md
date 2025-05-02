# Pair Trading Analysis Application

A comprehensive web-based application for analyzing and visualizing pair trading opportunities using statistical methods.

## Features

- Interactive web interface using Streamlit
- Asset pair selection with Yahoo Finance symbol search
- Comprehensive statistical analysis including:
  - Cointegration testing
  - Correlation analysis (Pearson and Spearman)
  - Granger causality testing (single and rolling)
  - Spread analysis with Z-score visualization
- Visualizations using Plotly
- Real-time data fetching from Yahoo Finance

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Starting the Application

1. Run the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

### 2. Basic Analysis

#### Example 1: Analyzing Bitcoin vs S&P 500
1. In the sidebar:
   - Search for "BTC" in the first asset field (select "BTC-USD - Bitcoin USD")
   - Search for "S&P" in the second asset field (select "^GSPC - S&P 500")
   - Set a date range (e.g., 2023-01-01 to 2025-01-01)
   - Click "Run Analysis"

#### Example 2: Analyzing Tech Stocks
1. In the sidebar:
   - Search for "Apple" in the first asset field (select "AAPL - Apple Inc.")
   - Search for "Microsoft" in the second asset field (select "MSFT - Microsoft Corporation")
   - Set a date range (e.g., 2023-01-01 to 2025-01-01)
   - Click "Run Analysis"

### 3. Interpreting Results

#### Price Series Analysis
- Compare the price movements of both assets
- Look for similar trends or divergences
- Use the interactive plot to zoom in on specific periods

#### Spread Analysis
- Observe the Z-score spread
- Look for mean reversion opportunities
- Note when the spread crosses the entry/exit levels (±1.5 and ±2.0)

#### Correlation Analysis
- Check the rolling Pearson correlation for linear relationships
- Examine the rolling Spearman correlation for monotonic relationships
- Look for periods of high correlation strength

#### Granger Causality
- Review the single Granger causality test results
- Analyze the rolling Granger causality plots
- Look for periods where one asset predicts the other

#### Comprehensive Analysis
- Review the long-term relationship assessment
- Check the short-term relationship analysis
- Evaluate the predictive relationship
- Consider the overall trading suitability rating

## Analysis Components

### 1. Price Series Analysis
- Visual comparison of both asset price series
- Interactive plot with hover information

### 2. Spread Analysis
- Z-score spread visualization
- Entry/Exit level indicators (±1.5 and ±2.0)
- Spread mean reversion analysis

### 3. Correlation Analysis
- Rolling Pearson correlation
- Rolling Spearman correlation
- Correlation strength interpretation

### 4. Granger Causality Analysis
- Single Granger causality test
- Rolling Granger causality analysis
- Statistical significance indicators

### 5. Comprehensive Analysis
- Long-term relationship assessment
- Short-term relationship analysis
- Predictive relationship evaluation
- Overall trading suitability rating

## Technical Requirements

- Python 3.12 or higher
- Required packages:
  - pandas
  - numpy
  - scikit-learn
  - yfinance
  - matplotlib
  - statsmodels
  - streamlit
  - plotly
  - seaborn
  - requests

## Project Structure

```
pair-trading/
├── app.py                 # Streamlit application
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── .gitignore            # Git ignore rules
├── pair_trading/
│   ├── __init__.py
│   ├── config.py         # Configuration settings
│   ├── main.py          # Main application logic
│   ├── pair_trading.py  # Core analysis functions
│   └── symbol_search.py # Yahoo Finance symbol search
└── README.md            # Project documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
