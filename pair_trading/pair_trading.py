import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint, grangercausalitytests
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from scipy.stats import spearmanr, pearsonr
import yfinance as yf
import matplotlib.pyplot as plt
from typing import Tuple, List

class PairTrading:
    def __init__(self, symbol1: str, symbol2: str, start_date: str, end_date: str):
        """
        Initialize PairTrading with two stock symbols and date range
        """
        self.symbol1 = symbol1
        self.symbol2 = symbol2
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.spread = None
        self.z_scores = None
        
    def fetch_data(self) -> pd.DataFrame:
        """
        Fetch historical data for both symbols
        """
        data1 = yf.download(self.symbol1, start=self.start_date, end=self.end_date)
        data2 = yf.download(self.symbol2, start=self.start_date, end=self.end_date)
        
        # Ensure both datasets have the same dates
        common_dates = data1.index.intersection(data2.index)
        
        # Create DataFrame with proper indexing
        self.data = pd.DataFrame({
            self.symbol1: data1.loc[common_dates, 'Close'].squeeze(),
            self.symbol2: data2.loc[common_dates, 'Close'].squeeze()
        }, index=common_dates)
        
        return self.data
    
    def calculate_spread(self) -> pd.Series:
        """
        Calculate the spread between the two assets
        """
        if self.data is None:
            self.fetch_data()
        
        self.spread = self.data[self.symbol1] - self.data[self.symbol2]
        return self.spread
    
    def calculate_z_scores(self) -> pd.Series:
        """
        Calculate z-scores of the spread
        """
        if self.spread is None:
            self.calculate_spread()
        
        mean = self.spread.mean()
        std = self.spread.std()
        self.z_scores = (self.spread - mean) / std
        return self.z_scores
    
    def test_cointegration(self) -> Tuple[float, float, float]:
        """
        Perform cointegration test
        Returns: (t-statistic, p-value, critical values)
        """
        if self.data is None:
            self.fetch_data()
        
        result = coint(self.data[self.symbol1], self.data[self.symbol2])
        return result

    def calculate_correlations(self) -> Tuple[float, float, float, float]:
        """
        Calculate Pearson and Spearman correlations
        Returns: (pearson_corr, pearson_p, spearman_corr, spearman_p)
        """
        if self.data is None:
            self.fetch_data()
        
        # Calculate Pearson correlation
        pearson_corr, pearson_p = pearsonr(self.data[self.symbol1], self.data[self.symbol2])
        
        # Calculate Spearman correlation
        spearman_corr, spearman_p = spearmanr(self.data[self.symbol1], self.data[self.symbol2])
        
        return pearson_corr, pearson_p, spearman_corr, spearman_p

    def test_granger_causality(self, window: int = None) -> Tuple[float, float, pd.Series, pd.Series]:
        """
        Perform Granger causality test
        If window is specified, performs rolling Granger causality
        Returns: (F-statistic, p-value, rolling_f_stats, rolling_p_values)
        """
        if self.data is None:
            self.fetch_data()
        
        if window is None:
            # Single test
            data = pd.DataFrame({
                'x': self.data[self.symbol1],
                'y': self.data[self.symbol2]
            })
            
            result = grangercausalitytests(data, maxlag=1)
            f_stat = result[1][0]['ssr_ftest'][0]
            p_value = result[1][0]['ssr_ftest'][1]
            
            return f_stat, p_value, None, None
        
        # Rolling Granger causality
        rolling_f_stats = []
        rolling_p_values = []
        
        for i in range(window, len(self.data)):
            window_data = pd.DataFrame({
                'x': self.data[self.symbol1].iloc[i-window:i],
                'y': self.data[self.symbol2].iloc[i-window:i]
            })
            
            try:
                result = grangercausalitytests(window_data, maxlag=1)
                f_stat = result[1][0]['ssr_ftest'][0]
                p_value = result[1][0]['ssr_ftest'][1]
                rolling_f_stats.append(f_stat)
                rolling_p_values.append(p_value)
            except:
                rolling_f_stats.append(np.nan)
                rolling_p_values.append(np.nan)
        
        rolling_f_stats = pd.Series(rolling_f_stats, index=self.data.index[window:])
        rolling_p_values = pd.Series(rolling_p_values, index=self.data.index[window:])
        
        return None, None, rolling_f_stats, rolling_p_values

    def plot_rolling_granger(self, window: int = 20) -> None:
        """
        Plot rolling Granger causality results
        """
        if self.data is None:
            self.fetch_data()
        
        # Get rolling Granger results
        _, _, rolling_f_stats, rolling_p_values = self.test_granger_causality(window)
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot F-statistics
        ax1.plot(rolling_f_stats, label=f'Rolling F-statistic (window={window})')
        ax1.axhline(3.84, color='red', linestyle='--', label='Critical value (95% confidence)')
        ax1.set_title(f'Rolling Granger Causality F-statistics')
        ax1.set_ylabel('F-statistic')
        ax1.legend()
        ax1.grid(True)
        
        # Plot p-values
        ax2.plot(rolling_p_values, label=f'Rolling p-value (window={window})')
        ax2.axhline(0.05, color='red', linestyle='--', label='Significance level')
        ax2.set_title(f'Rolling Granger Causality p-values')
        ax2.set_ylabel('p-value')
        ax2.set_xlabel('Date')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()

    def plot_rolling_correlations(self, window: int = 20) -> None:
        """
        Plot rolling correlations
        """
        if self.data is None:
            self.fetch_data()
        
        # Calculate rolling correlations
        rolling_pearson = self.data[self.symbol1].rolling(window=window).corr(self.data[self.symbol2])
        rolling_spearman = self.data[self.symbol1].rolling(window=window).apply(
            lambda x: spearmanr(x, self.data[self.symbol2].iloc[:len(x)])[0],
            raw=False
        )
        
        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(rolling_pearson, label=f'Rolling Pearson (window={window})')
        plt.plot(rolling_spearman, label=f'Rolling Spearman (window={window})')
        plt.axhline(0, color='black', linestyle='--')
        plt.title(f'Rolling Correlations: {self.symbol1} vs {self.symbol2}')
        plt.xlabel('Date')
        plt.ylabel('Correlation')
        plt.legend()
        plt.grid(True)
        plt.show()

    def analyze_relationship(self) -> None:
        """
        Perform comprehensive relationship analysis and save results
        """
        # Cointegration test
        t_stat, p_value, _ = self.test_cointegration()
        
        # Correlation analysis
        pearson_corr, pearson_p, spearman_corr, spearman_p = self.calculate_correlations()
        
        # Granger causality test
        f_stat, granger_p, _, _ = self.test_granger_causality()
        
        # Store interpretations as class attributes
        self.coint_interpretation = ""
        if abs(t_stat) > 2.0 and p_value < 0.05:
            self.coint_interpretation = "Long-term relationship exists"
        else:
            self.coint_interpretation = "No clear long-term relationship"
        
        self.corr_interpretation = ""
        if (abs(pearson_corr) >= 0.6 and pearson_p < 0.05) or (abs(spearman_corr) >= 0.6 and spearman_p < 0.05):
            self.corr_interpretation = "Strong relationship exists"
        else:
            self.corr_interpretation = "Weak or no relationship"
        
        self.causality_interpretation = ""
        if granger_p < 0.05:
            self.causality_interpretation = "One asset can predict the other"
        else:
            self.causality_interpretation = "No clear predictive relationship"
        
        self.trading_suitability = ""
        if (abs(t_stat) > 2.0 and p_value < 0.05) and \
           ((abs(pearson_corr) >= 0.6 and pearson_p < 0.05) or 
            (abs(spearman_corr) >= 0.6 and spearman_p < 0.05)):
            self.trading_suitability = "Excellent pair for trading"
        elif (abs(t_stat) > 1.5 and p_value < 0.1) and \
             ((abs(pearson_corr) >= 0.4 and pearson_p < 0.1) or 
              (abs(spearman_corr) >= 0.4 and spearman_p < 0.05)):
            self.trading_suitability = "Good pair for trading"
        else:
            self.trading_suitability = "Not suitable for trading"
        
        # Plot and save results
        self.plot_comprehensive_analysis()
        
        # Print results
        print("\nComprehensive Analysis:")
        print(f"1. Long-term relationship: {self.coint_interpretation}")
        print(f"2. Short-term relationship: {self.corr_interpretation}")
        print(f"3. Predictive relationship: {self.causality_interpretation}")
        print(f"\nOverall trading suitability: {self.trading_suitability}")
    
    def plot_comprehensive_analysis(self) -> None:
        """
        Plot comprehensive analysis including:
        - Price series
        - Spread and z-scores
        - Rolling correlations
        - Cointegration test results
        """
        if self.data is None:
            self.fetch_data()
        if self.z_scores is None:
            self.calculate_z_scores()
        
        # Create subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))
        
        # 1. Price series
        ax1.plot(self.data[self.symbol1], label=self.symbol1)
        ax1.plot(self.data[self.symbol2], label=self.symbol2)
        ax1.set_title(f"Price Series: {self.symbol1} vs {self.symbol2}")
        ax1.set_ylabel('Price')
        ax1.legend()
        ax1.grid(True)
        
        # 2. Spread and z-scores
        ax2.plot(self.z_scores, label='Z-Score')
        ax2.axhline(0, color='black', linestyle='--')
        ax2.axhline(1.5, color='red', linestyle='--', label='Entry Level')
        ax2.axhline(-1.5, color='red', linestyle='--')
        ax2.axhline(2.0, color='green', linestyle='--', label='Exit Level')
        ax2.axhline(-2.0, color='green', linestyle='--')
        ax2.set_title(f"Z-Score Spread: {self.symbol1} vs {self.symbol2}")
        ax2.set_ylabel('Z-Score')
        ax2.legend()
        ax2.grid(True)
        
        # 3. Rolling correlations
        window = 20
        rolling_pearson = self.data[self.symbol1].rolling(window=window).corr(self.data[self.symbol2])
        rolling_spearman = self.data[self.symbol1].rolling(window=window).apply(
            lambda x: spearmanr(x, self.data[self.symbol2].iloc[:len(x)])[0],
            raw=False
        )
        
        ax3.plot(rolling_pearson, label=f'Rolling Pearson (window={window})')
        ax3.plot(rolling_spearman, label=f'Rolling Spearman (window={window})')
        ax3.axhline(0, color='black', linestyle='--')
        ax3.set_title('Rolling Correlations')
        ax3.set_ylabel('Correlation')
        ax3.legend()
        ax3.grid(True)
        
        # 4. Cointegration and Granger causality results
        # Perform tests
        t_stat, p_value, _ = self.test_cointegration()
        f_stat, granger_p, _, _ = self.test_granger_causality()
        
        # Create text for results
        results_text = f"Cointegration Test:\n"\
                     f"t-statistic: {t_stat:.4f}\n"\
                     f"p-value: {p_value:.4f}\n\n"\
                     f"Granger Causality:\n"\
                     f"F-statistic: {f_stat:.4f}\n"\
                     f"p-value: {granger_p:.4f}\n\n"\
                     f"Comprehensive Analysis:\n"\
                     f"1. Long-term relationship: {self.coint_interpretation}\n"\
                     f"2. Short-term relationship: {self.corr_interpretation}\n"\
                     f"3. Predictive relationship: {self.causality_interpretation}\n\n"\
                     f"Overall trading suitability: {self.trading_suitability}"
        
        # Split text into two parts for better layout
        test_results = f"Cointegration Test:\n"\
                      f"t-statistic: {t_stat:.4f}\n"\
                      f"p-value: {p_value:.4f}\n\n"\
                      f"Granger Causality:\n"\
                      f"F-statistic: {f_stat:.4f}\n"\
                      f"p-value: {granger_p:.4f}"
        
        analysis_results = f"Comprehensive Analysis:\n"\
                          f"1. Long-term relationship: {self.coint_interpretation}\n"\
                          f"2. Short-term relationship: {self.corr_interpretation}\n"\
                          f"3. Predictive relationship: {self.causality_interpretation}\n\n"\
                          f"Overall trading suitability: {self.trading_suitability}"
        
        # Add test results
        ax4.text(0.05, 0.95, test_results, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Add analysis results
        ax4.text(0.05, 0.45, analysis_results, fontsize=12,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax4.axis('off')
        ax4.set_title('Test Results')
        
        plt.tight_layout()
        
        plt.show()

def main():
    # Example usage
    pair = PairTrading(
        symbol1="AAPL",
        symbol2="MSFT",
        start_date="2022-01-01",
        end_date="2023-12-31"
    )
    
    # Fetch data
    data = pair.fetch_data()
    
    # Test cointegration
    t_stat, p_value, _ = pair.test_cointegration()
    print(f"Cointegration test results:")
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    # Plot spread
    pair.plot_spread()

if __name__ == "__main__":
    main()
