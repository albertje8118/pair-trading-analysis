"""
Main entry point for pair trading strategy
"""

from pair_trading.pair_trading import PairTrading
from pair_trading.config import DEFAULT_START_DATE, DEFAULT_END_DATE

def main():
    # Get user input for symbols
    symbol1 = input("Enter first stock symbol (e.g. AAPL): ")
    symbol2 = input("Enter second stock symbol (e.g. MSFT): ")
    
    # Create pair trading instance
    pair = PairTrading(
        symbol1=symbol1,
        symbol2=symbol2,
        start_date=DEFAULT_START_DATE,
        end_date=DEFAULT_END_DATE
    )
    
    # Fetch and analyze data
    data = pair.fetch_data()
    print(f"\nData fetched for {symbol1} and {symbol2}")
    
    # Test cointegration
    t_stat, p_value, _ = pair.test_cointegration()
    print(f"\nCointegration test results:")
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    # Plot spread analysis
    pair.plot_spread()
    
    # TODO: Add trading logic implementation
    print("\nTrading logic will be implemented here")

if __name__ == "__main__":
    main()
