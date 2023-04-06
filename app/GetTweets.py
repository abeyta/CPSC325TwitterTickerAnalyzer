import os
import json
import pandas as pd
# from google.cloud import pubsub
import requests
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_keys.json"
with open("twitter_keys.json") as infile:
        twitter_keys = json.load(infile)
        token = twitter_keys["bearer_token"]

#define search twitter function
def search_twitter(query, tweet_fields, bearer_token = token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
        query, tweet_fields
    )
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

tweets = search_twitter("AAPL", "tweet.fields=created_at,text")
with open("tweets.json", "w") as write_file:
    json.dump(tweets, write_file, indent=4)



# # need to replace this with the path to your topic
# TOPIC_PATH = "projects/cloudfunctiondemo-376417/topics/tweets"

# class TweetStreamer(tweepy.StreamingClient):
#     def __init__(self, bearer_token):
#         super().__init__(bearer_token=bearer_token, wait_on_rate_limit=True)
    
#     def clear_and_set_filter_rules(self, filter_terms):
#         # clear out any existing rules
#         response = self.get_rules()
#         if response.data is not None:
#             rule_ids = [rule.id for rule in response.data]
#             self.delete_rules(rule_ids)
#         rules = [tweepy.StreamRule(term) for term in filter_terms]
#         self.add_rules(rules)
#         response = self.get_rules()
#         print("added number of rules:", len(response.data))

#     def on_connect(self):
#         print("Connection successful")

#     def on_disconnect(self):
#         print("Connection disconnected")

#     def on_tweet(self, tweet):
#         created_at = pd.Timestamp(tweet.created_at).strftime("%Y-%m-%d %H:%M:%S")
#         values = {"tweet_id": tweet.id, "author_id": tweet.author_id, "created_at": created_at, "text": tweet.text}
#         print(values)
#         publish_tweet(values)

# def publish_tweet(tweet_dict):
#     publisher_client = pubsub.PublisherClient()
#     tweet_str = json.dumps(tweet_dict).encode("utf-8")
#     future = publisher_client.publish(TOPIC_PATH, tweet_str)
#     print("published:", future.result())

# if __name__ == "__main__":
#     with open("twitter_keys.json") as infile:
#         twitter_keys = json.load(infile)
#         token = twitter_keys["bearer_token"]
#     streamer = TweetStreamer(token)
    
    
#     filter_terms = ["from:ZagMBB", "from:GinaSprint"]
#     streamer.clear_and_set_filter_rules(filter_terms)
    
#     streamer.filter(tweet_fields=["created_at", "author_id"])