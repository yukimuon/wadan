import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm
import pickle
import csv
import random
import tensorflow as tf
from tensorflow.keras import Sequential
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, LSTM, Embedding, Reshape
import tensorflow_datasets as tfds
import unidecode
from tensorflow.keras.preprocessing import sequence

url="https://raw.githubusercontent.com/tlkh/text-emotion-classification/master/data.csv"
import urllib.request
urllib.request.urlretrieve(url, "data.csv")
sentence=[]
sentiment=[]
texts=[]
with open("data.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        texts.append(row)
random.shuffle(texts)
for row in texts:
        sentence.append(row[0])
        sentiment.append(int(row[1]))

token =  tfds.features.text.Tokenizer()
vocab = [token.tokenize(x) for x in sentence]
vocab = list(set([y for x in vocab for y in x]))

encoder = tfds.features.text.SubwordTextEncoder(vocab_list=vocab)
print(tf.__version__)
path = os.path.join("sentany.h5")
print(path)
model = tf.keras.models.load_model(path)

import re
import csv
from datetime import date
day=str(date.today())
record=[0,0,0,0,0]
print("neutral, happy, sad, anger, hate.")
with open(day+'appledata.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        text=row[2]
        text=re.sub(r'http\S+', '', text)
        text=re.sub(r'[^\w\s]','',text)
        result=np.argmax(model.predict(sequence.pad_sequences([encoder.encode(text)])))
        record[result]=record[result]+1
        print(record,end="\r")
        

