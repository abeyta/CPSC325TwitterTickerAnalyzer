import os
import tensorflow as tf
from transformers import BertTokenizer
from pathlib import Path
from google.cloud import storage
from flask import jsonify
from json import JSONEncoder

def bert_model(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    data = request.get_json()
    tweets = data['tweets']
    download_model(request)
    twitter_model, tokenizer = load_model()
    if twitter_model: 
        predictions = predict_tweets(twitter_model, tokenizer, tweets)
        return jsonify(predictions)
    else:
        return jsonify("Failure")

def download_model(request):
    BUCKET_NAME = "twitter_bert_model"
    PROJECT_ID = "project-381921"
    working_dir = Path("/tmp")

    client = storage.Client(PROJECT_ID)
    bucket = client.get_bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()
    print(blobs)
    print("The bucket is established")

    for b in blobs:
        if str(b.name).startswith("bert_model/"):
            print("path download before")
            path_download = Path("/tmp").joinpath(b.name)
            print("WE IN:", path_download)
            if not path_download.parent.exists():
                path_download.parent.mkdir(parents=True)
                print("IN: NOT EXISTS")
                print(str(path_download))
            b.download_to_filename(str(path_download))

def load_model():
    twitter_model = tf.keras.models.load_model('/tmp/bert_model', compile=False)
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    return twitter_model, tokenizer

def predict_tweets(twitter_model, tokenizer, tweets):
    tf_batch = tokenizer(tweets, max_length=128, padding=True, truncation=True, return_tensors='tf')
    tf_outputs = twitter_model(tf_batch)
    tf_predictions = tf.nn.softmax(tf_outputs["logits"], axis=-1)
    labels = ['Negative','Positive']
    print(tf_predictions)
    label = tf.argmax(tf_predictions, axis=1)
    label = label.numpy()
    labeled = []
    for i in range(len(tweets)):
        labeled.append(labels[label[i]])
    return tweets, labeled, tf_predictions.numpy().tolist()