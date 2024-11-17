import streamlit as st

# Streamlit App - Main Screen
st.title("Welcome to the Options Pricing and Analysis Tool! 🎉")

# Greeting Section
st.header("👋 Hello, User!")
st.write("""
Welcome to the Options Pricing and Analysis Tool. This app helps you explore and visualize options pricing using the Black-Scholes-Merton model, 
analyze historical stock data, and gain deeper insights into market trends. 

Navigate using the sidebar to:
- 🧮 **Calculate Option Prices** using the Black-Scholes-Merton model.
- 📈 **Visualize Historical Data** for any stock ticker.
- 🌐 Explore advanced features and more!
""")

# Image or Branding (optional)
st.image("https://via.placeholder.com/800x200.png?text=Options+Pricing+Tool", use_column_width=True)

# Getting Started
st.header("Get Started 🚀")
st.write("""
1. Select a screen from the sidebar on the left.
2. Input the required details, such as the stock ticker and parameters.
3. View and interact with the results in real-time!

Don't forget to check out the 3D visualizations for a comprehensive analysis!
""")

# Footer Section
st.write("---")
st.write("💡 Pro Tip: Use the `Historical Visualizations` tab to explore long-term trends and make informed decisions.")

st.write("Enjoy exploring the world of options pricing and stock analysis! 📊")