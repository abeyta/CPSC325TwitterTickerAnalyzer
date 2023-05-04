import os
import json
import re
import pandas as pd
# from google.cloud import pubsub
import requests
import json
from sklearn.neighbors import KNeighborsClassifier as KNN

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_keys.json"
with open("twitter_keys.json") as infile:
        twitter_keys = json.load(infile)
        token = twitter_keys["bearer_token"]

URL = "https://us-central1-project-381921.cloudfunctions.net/model"

#define search twitter function
def search_twitter(query, tweet_fields, bearer_token = token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    print(query + " lang:en")
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query + " lang:en&max_results=50", tweet_fields
    )
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def clean_tweets(tweets):
    # Function to filter out tweets that have more than 2 tickers in the tweet
    tweets_list = []
    count = 0
    tickers_df = pd.read_csv("tickers.csv", index_col=0)
    for tweet in tweets["data"]:
        for ticker in tickers_df.index:
            result = tweet["text"].find(ticker)
            if result != -1:
                count += 1
        if count <= 3:
            # check for https links in the tweet
            result = tweet["text"].find("https")
            if result == -1:
                # if tweet containes a @tag, replace the tagged user with "USER"
                # this is to prevent the model from learning that a tweet with a tagged user is positive or negative  
                result = tweet["text"].find("@")
                if result != -1:
                    tweet["text"] = re.sub(r'{}.*?\s'.format('@'), '{} '.format('USER'), tweet["text"])
                    # tweet["text"] = tweet["text"][:result] + "USER" + tweet["text"][result+1:]
                tweets_list.append(tweet["text"])
        count = 0
    return tweets_list

def predict_tweets(ticker_picked, tweet_fields):
    tweets = search_twitter(ticker_picked, tweet_fields)
    tweets_list = []
    tweets = clean_tweets(tweets)
    for tweet in tweets:
        tweets_list.append(tweet)
    # make an http request to my cloud function
    headers = {"Content-Type": "application/json"}
    data = {"tweets": tweets_list}
    print(data)
    try:
        prediction = requests.post(URL, headers=headers, data=json.dumps(data))
        return prediction.json()
    except:
        return "Max memory limit reached."

def make_stock_prediction(X, y):
    KNNClassifier = KNN(n_neighbors=5)
    newX = [[x] for x in X]
    print(X.tolist())
    KNNClassifier.fit(X.tolist(), y)
    return KNNClassifier.predict([[0.5, 0.5]])
    
    