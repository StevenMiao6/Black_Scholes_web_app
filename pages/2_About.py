import streamlit as st

st.title('About This Streamlit Application')

st.markdown(""" 
Welcome to our interactive exploration of the Black-Scholes model! This application aims to demystify the Black-Scholes model, a cornerstone of financial mathematics that revolutionized the way we understand and price options. Our goal is to make this complex but powerful model accessible and useful to a broader audience.

# What is the Black-Scholes Model?
The Black-Scholes model, developed by Fischer Black, Myron Scholes, and Robert Merton in the early 1970s, provides a formula for calculating the theoretical price of options. It’s widely regarded as one of the most significant advancements in finance, laying the groundwork for modern options trading and risk management.

# Why Is It Important?
The model helps traders and investors determine the fair price of call and put options by considering factors like the current price of the underlying asset, the strike price of the option, the time to expiration, the risk-free interest rate, and the volatility of the asset. This enables more informed decision-making and effective risk management.

# Understanding Its Limitations
Despite its groundbreaking nature, the Black-Scholes model is not without its flaws. One significant limitation is its assumption of constant volatility. In reality, market volatility can fluctuate significantly over time, which can lead to discrepancies between the model’s predictions and actual market prices.

# Our Solution: Interactive Heatmaps
To address this limitation, we provide an interactive heatmap feature on our application. This tool allows you to visualize how changes in volatility and underlying asset price affect option pricing. By inputting different ranges for volatility and the underlying price, you can see how these factors influence the price of call and put options in real-time.

# How to Use This application
Explore the Black-Scholes Model: Use the sidebar to adjust the parameters of the Black-Scholes model and see how they affect option prices.
Visualize Volatility: Dive into our interactive heatmaps to understand how varying levels of volatility and underlying asset prices impact option pricing.
Calculate P&L: Input your purchase prices and compare them with the current model prices to calculate and visualize potential profit or loss.
We hope this tool helps you gain a deeper understanding of the Black-Scholes model and its practical applications. Whether you are a student, a trader, or simply curious about financial models, we invite you to explore and learn with us.

Happy exploring!
""")