import os
import tensorflow as tf
from transformers import BertTokenizer

def load_model():
    twitter_model = tf.keras.models.load_model('bert_model', compile=False)
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    # Check its architecture
    twitter_model.summary()
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
        print(label)
        labeled.append(labels[label[i]])
    return tweets, labeled

# model, token = load_model()
# predict_tweets(model, token, ["This was the worst movie I have ever seen"])
# predict_tweets(model, token, ["This was the best movie I have ever seen"])