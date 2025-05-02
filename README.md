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

1. Run the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. In the sidebar:
   - Enter or search for the first asset symbol
   - Enter or search for the second asset symbol
   - Select the date range for analysis
   - Click "Run Analysis" to perform the analysis

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
