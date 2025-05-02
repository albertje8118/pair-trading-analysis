import yfinance as yf
from typing import List, Tuple
import pandas as pd
import requests
import json
from typing import Optional

def search_symbols(query: str, max_results: int = 10) -> List[Tuple[str, str]]:
    """
    Search for Yahoo Finance symbols using a query
    Returns a list of tuples containing (symbol, name)
    """
    try:
        # Use Yahoo Finance's search endpoint
        url = f'https://query2.finance.yahoo.com/v1/finance/search?q={query}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []
            
        data = response.json()
        quotes = data.get('quotes', [])
        
        results = []
        for quote in quotes[:max_results]:
            symbol = quote.get('symbol')
            name = quote.get('shortname') or quote.get('longname')
            if symbol and name:
                results.append((symbol, name))
                
        return results
        
    except Exception as e:
        print(f"Error searching symbols: {str(e)}")
        return []

def get_symbol_info(symbol: str) -> Optional[dict]:
    """
    Get detailed information about a symbol
    Returns a dictionary with symbol information or None if not found
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return info
    except:
        return None
