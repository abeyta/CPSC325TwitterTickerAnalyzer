import json
import streamlit as st
import pandas as pd
import GetStockInfo as gsi
import GetTweets as gt
import plotly.express as px

st.title("Twitter Ticker Analyzer")
st.write("This is a simple app to analyze the sentiment of tweets about a stock ticker.")
tickers_df = pd.read_csv("tickers.csv", index_col=0)
ticker_picked = st.selectbox("Pick a ticker", tickers_df.index)
stock_figure = gsi.get_stock_figure(ticker_picked)
st.plotly_chart(stock_figure)
predictions = gt.predict_tweets(ticker_picked, "tweet.fields=created_at,text")
if predictions == "Max memory limit reached.":
    st.write(predictions)
    st.stop()
else: 
    # write predictions to streamlit app
    data = pd.DataFrame(predictions).T
    # plotly chart to show predictions in the 3rd column of the data frame
    # grab the 3rd column of the data frame
    tensor_data = data.iloc[:, 2]
    labels = data.iloc[:, 1]

    print(labels)
    x = []
    y = []
    for row in tensor_data:
        print(row[0])
        x.append(row[0])
        y.append(row[1])
    print(x)
    print(y)
    # , columns=['tweets', 'sentiment']
    chart_data = pd.DataFrame(x, y)
    # st.write(chart_data)
    fig = px.scatter(x=x, y=y)
    final = gt.make_stock_prediction(tensor_data, labels)
    st.write('Tweet Sentiment Predictions: ' + final)
    st.write(fig)
    st.write(data)
