import streamlit as st
import yfinance as yf
import numpy as np
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.express as px

# Black-Scholes-Merton formula
def black_scholes(S, X, T, r, sigma, q=0):
    d1 = (np.log(S / X) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call = S * np.exp(-q * T) * norm.cdf(d1) - X * np.exp(-r * T) * norm.cdf(d2)
    put = X * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    return call, put

# Streamlit App
st.title("Black-Scholes-Merton Options Pricing Model")

# Sidebar Navigation
menu = ["BSM Model", "Historical Visualizations"]
choice = st.sidebar.selectbox("Select a Screen", menu)

if choice == "BSM Model":
    # User Inputs for Ticker and Strike Price
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")
    X = st.number_input("Strike Price (X)", min_value=0.0, value=100.0)
    T = st.number_input("Time to Maturity (T in years)", min_value=0.01, value=1.0)

    # Fetch Data Using yfinance
    try:
        stock = yf.Ticker(ticker)
        stock_price = stock.history(period="1d")["Close"].iloc[-1]
        st.write(f"Current Stock Price for {ticker}: ${stock_price:.2f}")
        
        # Assuming fixed values for simplicity
        r = 0.05  # Risk-free rate
        sigma = 0.2  # Volatility
        q = 0.0  # Dividend yield

        # Calculate Option Prices
        call, put = black_scholes(stock_price, X, T, r, sigma, q)

        # Display Results
        st.write(f"Call Option Price: ${call:.2f}")
        st.write(f"Put Option Price: ${put:.2f}")

        # 3D Visualization
        if st.checkbox("Show 3D Plot"):
            S_range = np.linspace(stock_price * 0.5, stock_price * 1.5, 50)
            T_range = np.linspace(0.01, 2, 50)
            S_grid, T_grid = np.meshgrid(S_range, T_range)
            Call_prices = np.array([black_scholes(S, X, t, r, sigma, q)[0] for S, t in zip(S_grid.ravel(), T_grid.ravel())])
            Call_prices = Call_prices.reshape(S_grid.shape)

            fig = go.Figure(data=[go.Surface(z=Call_prices, x=S_range, y=T_range)])
            fig.update_layout(title="Call Option Prices", scene=dict(
                xaxis_title="Stock Price (S)",
                yaxis_title="Time to Maturity (T)",
                zaxis_title="Option Price"))
            st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Error fetching data for ticker {ticker}: {e}")

elif choice == "Historical Visualizations":
    # Historical Visualization Screen
    ticker = st.text_input("Enter Stock Ticker for Historical Data (e.g., AAPL, TSLA)", value="AAPL")
    period = st.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"])
    interval = st.selectbox("Select Interval", ["1d", "5d", "1wk", "1mo", "3mo"])

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)

        if not hist.empty:
            st.write(f"Historical Data for {ticker}")
            fig = px.line(hist, x=hist.index, y="Close", title=f"{ticker} Historical Close Prices")
            st.plotly_chart(fig)

            st.write("Statistical Overview")
            st.write(hist.describe())
        else:
            st.error("No historical data found for the selected ticker and period.")
    except Exception as e:
        st.error(f"Error fetching historical data for ticker {ticker}: {e}")