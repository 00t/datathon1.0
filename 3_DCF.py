import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# DCF Calculation Function
def calculate_dcf(fcf, growth_rate, discount_rate, terminal_rate, years=5):
    fcf_values = [fcf * (1 + growth_rate) ** i for i in range(1, years + 1)]
    terminal_value = fcf_values[-1] * (1 + terminal_rate) / (discount_rate - terminal_rate)
    discounted_fcf = [value / (1 + discount_rate) ** i for i, value in enumerate(fcf_values, start=1)]
    discounted_terminal_value = terminal_value / (1 + discount_rate) ** years
    return sum(discounted_fcf) + discounted_terminal_value, fcf_values, discounted_fcf, terminal_value

# Streamlit App
st.title("Enhanced Discounted Cash Flow (DCF) Analysis 📊")

# Sidebar Inputs
st.sidebar.header("DCF Parameters")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")
growth_rate = st.sidebar.slider("Revenue Growth Rate (%)", 0, 20, 5) / 100
discount_rate = st.sidebar.slider("Discount Rate (%)", 0, 20, 10) / 100
terminal_rate = st.sidebar.slider("Terminal Growth Rate (%)", 0, 10, 2) / 100
years = st.sidebar.slider("Projection Years", 1, 10, 5)

# Define thresholds
MIN_FCF = 100000000  # Minimum Free Cash Flow ($)

# Fetch Historical Data
try:
    stock = yf.Ticker(ticker)
    cashflow = stock.cashflow

    # Extract Free Cash Flow (FCF)
    try:
        fcf_operating = cashflow.loc['Total Cash From Operating Activities'].iloc[0]
        fcf_capex = cashflow.loc['Capital Expenditures'].iloc[0]
        fcf = fcf_operating + fcf_capex  # CapEx is usually negative
        st.sidebar.write(f"Latest Free Cash Flow (FCF) for {ticker}: ${fcf:,.2f}")

        if fcf < MIN_FCF:
            st.warning(f"Warning: The Free Cash Flow is below the minimum threshold of ${MIN_FCF:,.2f}. Proceeding with available data.")
    except KeyError:
        st.sidebar.error("Missing FCF data. Please input manually.")
        fcf = st.sidebar.number_input("Enter Free Cash Flow Manually", value=MIN_FCF)

    # Calculate DCF
    dcf_value, fcf_values, discounted_fcf, terminal_value = calculate_dcf(fcf, growth_rate, discount_rate, terminal_rate, years)
    st.header(f"Intrinsic Value Estimate for {ticker}")
    st.metric(label="DCF Value", value=f"${dcf_value:,.2f}")

    # Cash Flow Timeline
    st.subheader("Projected Cash Flow Timeline")
    cash_flow_data = pd.DataFrame({
        "Year": range(1, years + 1),
        "Future Cash Flow": fcf_values,
        "Discounted Cash Flow": discounted_fcf
    })
    fig_timeline = px.bar(cash_flow_data, x="Year", y=["Future Cash Flow", "Discounted Cash Flow"],
                          barmode="group", title="Cash Flow Timeline")
    st.plotly_chart(fig_timeline)

    # Waterfall Chart
    st.subheader("Waterfall Chart of Value Components")
    waterfall_data = [
        {"label": "Discounted Cash Flows", "value": sum(discounted_fcf)},
        {"label": "Terminal Value", "value": terminal_value},
        {"label": "Intrinsic Value", "value": dcf_value}
    ]
    waterfall_fig = go.Figure(go.Waterfall(
        x=[d["label"] for d in waterfall_data],
        y=[d["value"] for d in waterfall_data],
        connector=dict(line=dict(color="rgb(63, 63, 63)")),
    ))
    waterfall_fig.update_layout(title="Value Components", showlegend=False)
    st.plotly_chart(waterfall_fig)

    # Sensitivity Heatmap
    st.subheader("Sensitivity Analysis Heatmap")
    growth_rates = np.linspace(0.01, 0.2, 10)
    discount_rates = np.linspace(0.05, 0.2, 10)
    heatmap_values = np.zeros((len(growth_rates), len(discount_rates)))

    for i, g in enumerate(growth_rates):
        for j, d in enumerate(discount_rates):
            heatmap_values[i, j], _, _, _ = calculate_dcf(fcf, g, d, terminal_rate, years)

    heatmap_fig = px.imshow(heatmap_values, x=np.round(discount_rates, 2), y=np.round(growth_rates, 2),
                            labels={'x': 'Discount Rate', 'y': 'Growth Rate', 'color': 'DCF Value'},
                            title="DCF Value Sensitivity to Growth & Discount Rates")
    st.plotly_chart(heatmap_fig)

    # Tornado Chart
    st.subheader("Tornado Chart: Sensitivity to Parameters")
    parameters = ["Growth Rate", "Discount Rate", "Terminal Growth Rate"]
    base_dcf = dcf_value
    tornado_data = []
    for param, base_val, delta in zip(parameters, [growth_rate, discount_rate, terminal_rate], [0.01, 0.01, 0.005]):
        plus, _, _, _ = calculate_dcf(fcf, growth_rate + (delta if param == "Growth Rate" else 0),
                                      discount_rate + (delta if param == "Discount Rate" else 0),
                                      terminal_rate + (delta if param == "Terminal Growth Rate" else 0), years)
        minus, _, _, _ = calculate_dcf(fcf, growth_rate - (delta if param == "Growth Rate" else 0),
                                       discount_rate - (delta if param == "Discount Rate" else 0),
                                       terminal_rate - (delta if param == "Terminal Growth Rate" else 0), years)
        tornado_data.append({"Parameter": param, "Impact": plus - minus})

    tornado_df = pd.DataFrame(tornado_data)
    tornado_fig = px.bar(tornado_df, x="Impact", y="Parameter", orientation="h", title="Sensitivity to Parameters")
    st.plotly_chart(tornado_fig)

except Exception as e:
    st.error(f"Error fetching data for ticker {ticker}: {e}")