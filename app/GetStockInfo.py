import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

def get_stock_figure(ticker):
    # load tickers from csv
    df = pd.read_csv("tickers.csv", index_col=0)
    # print(df)

    # import ticker data
    # for ticker in df.index:
    #     # print(ticker)
    #     data = yf.download(tickers=ticker, period="1d", interval="1m")
    #     # print(data)
    data = yf.download(tickers=ticker[1:], period="1d", interval="1m")
    print(data)

    # declare figure
    fig = go.Figure()

    # Candlestick
    fig.add_trace(go.Candlestick(x=data.index,
                                open=data['Open'],
                                high=data['High'],
                                low=data['Low'],
                                close=data['Close'], name='market data'))

    # Add titles
    fig.update_layout(
        title='{} live share price evolution'.format(ticker),
        yaxis_title='Stock Price (USD per Shares)')

    # X-Axes
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=3, label="3h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return fig