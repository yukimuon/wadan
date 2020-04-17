from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import numpy as np
import matplotlib.pyplot as plt
import os
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
import pickle

path = os.path.join("Model_5.h5")
print(path)
model = tf.keras.models.load_model(path)

sentence=[]
sentiment=[]
texts=[]
with open("traindata.csv") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row not in texts:
            texts.append(row)
random.shuffle(texts)
print(texts[12])
for row in texts:
    sentence.append(row[0])
    sentiment.append(int(row[1]))
from tensorflow.keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=40000)
tokenizer.fit_on_texts(sentence)
from tensorflow.keras.preprocessing.sequence import pad_sequences
sentence_token = tokenizer.texts_to_sequences(sentence)

def process(text):
    text_p = tokenizer.texts_to_sequences([text])
    processed = pad_sequences(text_p)
    return processed

import re
import csv
from datetime import date

prefix="data/2020-04-"
dayrec={}
for i in range(1,13):
    if i<10:
        day="0"+str(i)
    else:
        day=str(i)
    with open(prefix+day+".csv", newline='') as csvfile:
        record=[0,0,0,0,0,0]
        reader = csv.reader(csvfile)
        for row in reader:
            text=row[2]
            re.sub(r'[^\x00-\x7F]+',' ', text)
            if "http" in text:
                continue
            else:
                text=re.sub(r'[^\w\s]','',text)
                try:
                    result=np.argmax(model.predict(process(text)))
                except:
                    result=5
                record[result]=record[result]+1
                print(record,end="\r")
        dayrec[prefix+day+".csv"]=record

    with open(prefix+day+"appledata.csv", newline='') as csvfile:
        record=[0,0,0,0,0,0]
        reader = csv.reader(csvfile)
        for row in reader:
            text=row[2]
            re.sub(r'[^\x00-\x7F]+',' ', text)
            if "http" in text:
                continue
            else:
                text=re.sub(r'[^\w\s]','',text)
                try:
                    result=np.argmax(model.predict(process(text)))
                except:
                    result=5                
                record[result]=record[result]+1
                print(record,end="\r")
        dayrec[prefix+day+"appledata.csv"]=record

    with open("dayrec.pickle", "wb") as handle:
        pickle.dump(dayrec,handle)
        handle.close()