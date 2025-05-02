"""
Configuration settings for pair trading
"""

# Default trading parameters
ENTRY_THRESHOLD = 1.5  # Z-score threshold for entry
EXIT_THRESHOLD = 2.0   # Z-score threshold for exit

# Risk management
MAX_POSITION_SIZE = 0.1  # Maximum position size as % of portfolio
STOP_LOSS = 0.02        # Stop loss level (2%)

# Backtesting parameters
INITIAL_CAPITAL = 100000  # Initial capital for backtesting
COMMISSION = 0.001       # Trading commission (0.1%)

# Data parameters
DEFAULT_START_DATE = "2022-01-01"
DEFAULT_END_DATE = "2023-12-31"

# Cointegration test parameters
COINT_SIGNIFICANCE_LEVEL = 0.05  # 95% confidence level

# Plotting parameters
PLOT_WINDOW = 200  # Number of days to show in plots
Z_SCORE_COLORS = {
    'entry_long': 'red',
    'entry_short': 'red',
    'exit': 'green'
}
