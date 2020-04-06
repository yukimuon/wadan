from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from absl import logging
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.datasets import imdb
import tweepy
import pickle
import random
import json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer


def load_directory_data(directory):
  data = {}
  data["sentence"] = []
  data["sentiment"] = []
  for file_path in os.listdir(directory):
    with tf.io.gfile.GFile(os.path.join(directory, file_path), "r") as f:
      data["sentence"].append(f.read())
      data["sentiment"].append(re.match("\d+_(\d+)\.txt", file_path).group(1))
  return pd.DataFrame.from_dict(data)

def load_dataset(directory):
  pos_df = load_directory_data(os.path.join(directory, "pos"))
  neg_df = load_directory_data(os.path.join(directory, "neg"))
  pos_df["polarity"] = 1
  neg_df["polarity"] = 0
  return pd.concat([pos_df, neg_df]).sample(frac=1).reset_index(drop=True)

def download_and_load_datasets(force_download=False):
  dataset = tf.keras.utils.get_file(
      fname="aclImdb.tar.gz", 
      origin="http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz", 
      extract=True)
  
  train_df = load_dataset(os.path.join(os.path.dirname(dataset), 
                                       "aclImdb", "train"))
  test_df = load_dataset(os.path.join(os.path.dirname(dataset), 
                                      "aclImdb", "test"))
  
  return train_df, test_df
logging.set_verbosity(logging.ERROR)

train_df, test_df = download_and_load_datasets()

data_x=list(train_df.get("sentence"))
datate_x=list(test_df.get("sentence"))
def delp(string): 
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in string.lower(): 
        if x in punctuations: 
            string = string.replace(x, "") 
    return string
import string
pr_train=[]
pr_test=[]
for x in data_x:
    x.replace("<br /><br />","")
    x.replace(r"\n", " ")
    pr_train.append(delp(x))
for x in datate_x:
    x.replace("<br /><br />","")
    x.replace(r"\n", "")
    pr_test.append(delp(x))
sentence = pr_train + pr_test
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(sentence)

train_x = pad_sequences(tokenizer.texts_to_sequences(pr_train), maxlen=80)

def process(text):
    return pad_sequences(tokenizer.texts_to_sequences([text]), maxlen=80)

index=0
pos=0
def init():
    f = open("apikey", "r")
    f.readline()
    key0=f.readline().split(",")
    f.close()
    model = tf.keras.models.load_model('Model_bin.h5')


    def getAuth(key):
        auth = tweepy.OAuthHandler(key[0], key[1])
        auth.set_access_token(key[2], key[3])
        return auth

    class Listener(tweepy.StreamListener):
        def on_data(self, data):
            par= json.loads(data)
            global index,pos
            try:
                text=par["text"]
                text.replace("<br /><br />","")
                text.replace(r"\n", " ")
                text_p=delp(text)
                index+=1
                score=model.predict(process(text_p))[0][0]
                if score>0.5:
                    pos+=1
                print(pos/index,end='\r')
            except:
                pass

        def error(self, status):
            print(status)

    auth=getAuth(key0)
    l = Listener()
    stream = tweepy.Stream(auth, l)
    stream.filter(track=["ipad","macbook","iphone","macbookpro","macbookair","apple","samsung","huawei","oneplus"],languages=["en"])
    return 1

init()