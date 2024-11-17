import streamlit as st
import yfinance as yf
import plotly.express as px

# Fetch Stock Profile
def fetch_stock_profile(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    # Extract key metrics
    profile_data = {
        "Company Name": info.get("longName", "N/A"),
        "Sector": info.get("sector", "N/A"),
        "Industry": info.get("industry", "N/A"),
        "Country": info.get("country", "N/A"),
        "Current Price": info.get("currentPrice", "N/A"),
        "Market Cap": f"${info.get('marketCap', 0):,}" if info.get('marketCap') else "N/A",
        "Beta": info.get("beta", "N/A"),
        "Dividend Yield": f"{info.get('dividendYield', 0) * 100:.2f}%" if info.get('dividendYield') else "N/A",
        "P/E Ratio": info.get("trailingPE", "N/A"),
        "EV/EBITDA": info.get("enterpriseToEbitda", "N/A"),
        "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
        "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
    }
    return profile_data, stock.history(period="1y")

# Main Profile Module
st.sidebar.header("Stock Profile")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")

if ticker:
    try:
        # Fetch data
        profile_data, history_data = fetch_stock_profile(ticker)

        # Display Profile
        st.header(f"Profile: {profile_data['Company Name']} ({ticker.upper()})")
        for key, value in profile_data.items():
            st.write(f"**{key}:** {value}")

        # Key Feature Analysis
        st.subheader("Key Feature Analysis")

        # Price Trend
        st.write("**Price Trend (Last Year):**")
        fig_price_trend = px.line(history_data, x=history_data.index, y="Close", title=f"{ticker.upper()} Price Trend")
        st.plotly_chart(fig_price_trend)

        # Volume Trend
        st.write("**Volume Trend (Last Year):**")
        fig_volume_trend = px.bar(history_data, x=history_data.index, y="Volume", title=f"{ticker.upper()} Volume Trend")
        st.plotly_chart(fig_volume_trend)

    except Exception as e:
        st.error(f"Could not fetch data for {ticker.upper()}: {e}")