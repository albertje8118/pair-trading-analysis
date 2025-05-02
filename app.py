import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pair_trading.pair_trading import PairTrading
from pair_trading.symbol_search import search_symbols
from scipy.stats import spearmanr

# Page configuration
st.set_page_config(
    page_title="Pair Trading Analysis",
    page_icon="📊",
    layout="wide"
)

# Sidebar configuration
st.sidebar.header("Pair Trading Analysis")

# Input parameters
# Symbol search for first asset
st.sidebar.subheader("Select First Asset")
search_query1 = st.sidebar.text_input("Search for first asset (e.g., BTC, Apple)", "")
if search_query1:
    results1 = search_symbols(search_query1)
    if results1:
        symbol1 = st.sidebar.selectbox(
            "Select first asset",
            options=[f"{symbol} - {name}" for symbol, name in results1],
            format_func=lambda x: x.split(" - ")[1]
        )
    else:
        symbol1 = st.sidebar.text_input("First Symbol (e.g., BTC-USD)", value="BTC-USD")
else:
    symbol1 = st.sidebar.text_input("First Symbol (e.g., BTC-USD)", value="BTC-USD")

# Symbol search for second asset
st.sidebar.subheader("Select Second Asset")
search_query2 = st.sidebar.text_input("Search for second asset (e.g., NDX, Microsoft)", "")
if search_query2:
    results2 = search_symbols(search_query2)
    if results2:
        symbol2 = st.sidebar.selectbox(
            "Select second asset",
            options=[f"{symbol} - {name}" for symbol, name in results2],
            format_func=lambda x: x.split(" - ")[1]
        )
    else:
        symbol2 = st.sidebar.text_input("Second Symbol (e.g., ^NDX)", value="^NDX")
else:
    symbol2 = st.sidebar.text_input("Second Symbol (e.g., ^NDX)", value="^NDX")
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-05-02"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2025-05-02"))

# Run analysis button
if st.sidebar.button("Run Analysis"):
    try:
        # Extract just the symbol from the selected option
        if isinstance(symbol1, str) and " - " in symbol1:
            symbol1 = symbol1.split(" - ")[0]
        if isinstance(symbol2, str) and " - " in symbol2:
            symbol2 = symbol2.split(" - ")[0]
            
        # Create PairTrading instance
        pair = PairTrading(symbol1, symbol2, str(start_date), str(end_date))
        
        # Run analysis
        pair.analyze_relationship()
        
        # Get results
        t_stat, p_value, _ = pair.test_cointegration()
        pearson_corr, pearson_p, spearman_corr, spearman_p = pair.calculate_correlations()
        f_stat, granger_p, _, _ = pair.test_granger_causality()
        
        # Create main content
        st.title("Pair Trading Analysis")
        st.write(f"Analyzing {symbol1} vs {symbol2}")
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Price Series", "Spread Analysis", "Correlation Analysis", "Granger Causality", "Test Results"])
        
        # Tab 1: Price Series
        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=pair.data.index, y=pair.data[symbol1], name=symbol1))
            fig.add_trace(go.Scatter(x=pair.data.index, y=pair.data[symbol2], name=symbol2))
            fig.update_layout(
                title="Price Series Comparison",
                yaxis_title="Price",
                xaxis_title="Date",
                legend_title="Assets"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Tab 2: Spread Analysis
        with tab2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=pair.z_scores.index, y=pair.z_scores, name="Z-Score"))
            fig.add_hline(y=0, line_dash="dash", line_color="black")
            fig.add_hline(y=1.5, line_dash="dash", line_color="red", name="Entry Level")
            fig.add_hline(y=-1.5, line_dash="dash", line_color="red")
            fig.add_hline(y=2.0, line_dash="dash", line_color="green", name="Exit Level")
            fig.add_hline(y=-2.0, line_dash="dash", line_color="green")
            fig.update_layout(
                title="Z-Score Spread Analysis",
                yaxis_title="Z-Score",
                xaxis_title="Date"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Tab 3: Correlation Analysis
        with tab3:
            window = 20
            rolling_pearson = pair.data[symbol1].rolling(window=window).corr(pair.data[symbol2])
            rolling_spearman = pair.data[symbol1].rolling(window=window).apply(
                lambda x: spearmanr(x, pair.data[symbol2].iloc[:len(x)])[0],
                raw=False
            )
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=rolling_pearson.index, y=rolling_pearson, name=f'Rolling Pearson (window={window})'))
            fig.add_trace(go.Scatter(x=rolling_spearman.index, y=rolling_spearman, name=f'Rolling Spearman (window={window})'))
            fig.add_hline(y=0, line_dash="dash", line_color="black")
            fig.update_layout(
                title="Rolling Correlations",
                yaxis_title="Correlation",
                xaxis_title="Date"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Tab 4: Granger Causality Analysis
        with tab4:
            st.subheader("Granger Causality Analysis")
            
            # Single Granger test
            f_stat, p_value, _, _ = pair.test_granger_causality()
            st.write("**Single Granger Causality Test**")
            st.write(f"F-statistic: {f_stat:.4f}")
            st.write(f"p-value: {p_value:.4f}")
            
            # Rolling Granger test
            window = 20
            _, _, rolling_f_stats, rolling_p_values = pair.test_granger_causality(window)
            
            # Create plots
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=rolling_f_stats.index, y=rolling_f_stats, name=f'Rolling F-statistic (window={window})'))
            fig.add_hline(y=3.84, line_dash="dash", line_color="red", name='Critical value (95% confidence)')
            fig.update_layout(
                title="Rolling Granger Causality F-statistics",
                yaxis_title="F-statistic",
                xaxis_title="Date"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=rolling_p_values.index, y=rolling_p_values, name=f'Rolling p-value (window={window})'))
            fig.add_hline(y=0.05, line_dash="dash", line_color="red", name='Significance level')
            fig.update_layout(
                title="Rolling Granger Causality p-values",
                yaxis_title="p-value",
                xaxis_title="Date"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Tab 5: Test Results
        with tab5:
            st.subheader("Statistical Tests")
            
            # Cointegration Test
            st.write("**Cointegration Test**")
            st.write(f"t-statistic: {t_stat:.4f}")
            st.write(f"p-value: {p_value:.4f}")
            
            # Correlation Results
            st.write("\n**Correlation Analysis**")
            st.write(f"Pearson correlation: {pearson_corr:.4f} (p-value: {pearson_p:.4f})")
            st.write(f"Spearman correlation: {spearman_corr:.4f} (p-value: {spearman_p:.4f})")
            
            # Granger Causality
            st.write("\n**Granger Causality Test**")
            st.write(f"F-statistic: {f_stat:.4f}")
            st.write(f"p-value: {granger_p:.4f}")
            
            # Comprehensive Analysis
            st.write("\n**Comprehensive Analysis**")
            st.write(f"1. Long-term relationship: {pair.coint_interpretation}")
            st.write(f"2. Short-term relationship: {pair.corr_interpretation}")
            st.write(f"3. Predictive relationship: {pair.causality_interpretation}")
            st.write(f"\nOverall trading suitability: {pair.trading_suitability}")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
