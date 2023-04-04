import streamlit as st
import pandas as pd
import GetStockInfo as gsi
import GetTweets as gt

st.title("Twitter Ticker Analyzer")
st.write("This is a simple app to analyze the sentiment of tweets about a stock ticker.")
tickers_df = pd.read_csv("tickers.csv", index_col=0)
ticker_picked = st.selectbox("Pick a ticker", tickers_df.index)
stock_figure = gsi.get_stock_figure(ticker_picked)
st.plotly_chart(stock_figure)
st.write(gt.search_twitter(ticker_picked, "tweet.fields=created_at,text"))