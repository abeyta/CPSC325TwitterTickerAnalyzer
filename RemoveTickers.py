import pandas as pd

tickers_df = pd.read_csv("tickers.csv", index_col=0)

# remove all rows from the dataframe that are not Sectors of Information Technology or Communication Services
tickers_df = tickers_df[(tickers_df["Sector"] == "Information Technology") | (tickers_df["Sector"] == "Communication Services")]
# print out the new dataframe
print(tickers_df)
# write to a new csv file
tickers_df.to_csv("tickers.csv")
