import streamlit as st
import pandas as pd
import GetStockInfo as gsi

st.title("Twitter Ticker Analyzer")
st.write("This is a simple app to analyze the sentiment of tweets about a stock ticker.")
ticker_picked = st.selectbox("Pick a ticker", ["$TSLA", "$AAPL", "$AMZN", "$NVDA"])
stock_figure = gsi.get_stock_figure(ticker_picked)
st.plotly_chart(stock_figure)