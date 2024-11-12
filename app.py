import streamlit as st
import requests
import pandas as pd
import numpy as np

# Define the top companies and their ticker symbols
top_companies = {
    'apple': 'AAPL',
    'microsoft': 'MSFT',
    'google': 'GOOGL',
    'amazon': 'AMZN',
    'tesla': 'TSLA',
    'facebook': 'FB',
    'nvidia': 'NVDA',
    'berkshire hathaway': 'BRK.B',
    'visa': 'V',
    'jpmorgan': 'JPM',
    'unitedhealth': 'UNH',
    'procter & gamble': 'PG',
    'mastercard': 'MA',
    'coca-cola': 'KO',
    'pepsico': 'PEP',
    'walmart': 'WMT',
    'exxon mobil': 'XOM',
    'home depot': 'HD',
    'pfizer': 'PFE',
    'intel': 'INTC',
    'salesforce': 'CRM',
    'abbvie': 'ABBV',
    'broadcom': 'AVGO',
    'adobe': 'ADBE',
    'nike': 'NKE',
    'caterpillar': 'CAT',
    'starbucks': 'SBUX',
    'boeing': 'BA',
    'costco': 'COST',
    'merck': 'MRK',
    'thermo fisher': 'TMO'
}

# Function to get ticker from input
def get_company_name_from_input(input):
    for key in top_companies:
        if key in input.lower():
            return top_companies[key]
    return input  # Assume the input is a ticker symbol if not found

# Alpha Vantage API key
API_KEY = "K0AWNF84KI0CAX1L"

# Function to get stock price data
def get_stock_price(ticker):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    try:
        last_price = float(list(data["Time Series (5min)"].values())[0]["4. close"])
        return {
            'ticker': ticker,
            'price': last_price
        }
    except KeyError:
        return None

# Calculate RSI, EMA, SMA, and MACD
def calculate_technical_indicators(ticker):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    try:
        # Convert the JSON data to a pandas DataFrame
        df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index", dtype=float)
        df.columns = ["open", "high", "low", "close", "volume"]
        df = df.sort_index()

        # RSI Calculation
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # EMA Calculation
        ema = df["close"].ewm(span=20, adjust=False).mean()

        # SMA Calculation
        sma = df["close"].rolling(window=50).mean()

        # MACD Calculation
        exp1 = df["close"].ewm(span=12, adjust=False).mean()
        exp2 = df["close"].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2

        # Returning latest values
        return {
            "RSI": rsi.iloc[-1],
            "EMA": ema.iloc[-1],
            "SMA": sma.iloc[-1],
            "MACD": macd.iloc[-1]
        }
    except KeyError:
        return None

# Streamlit UI
st.title("Stock Price App")
user_input = st.text_input("Ask about a stock...")

if st.button("Get Stock Price"):
    company_name = get_company_name_from_input(user_input)
    stock_data = get_stock_price(company_name)

    if stock_data:
        st.write(f"The current price of **{company_name}** ({stock_data['ticker']}) is **${stock_data['price']:.2f}**")
    else:
        st.error(f"Data retrieval issue: {e}")
        
if st.button("Get Technical Indicators"):
    company_name = get_company_name_from_input(user_input)
    indicators = calculate_technical_indicators(company_name)

    if indicators:
        st.write(f"The current RSI for **{company_name}** is **{indicators['RSI']:.2f}**")
        st.write(f"The current EMA for **{company_name}** is **{indicators['EMA']:.2f}**")
        st.write(f"The current SMA for **{company_name}** is **{indicators['SMA']:.2f}**")
        st.write(f"The current MACD for **{company_name}** is **{indicators['MACD']:.2f}**")
    else:
        st.error(f"Data retrieval issue: {e}")
