#! /usr/bin/python3

import time
import tweepy
import pickle
import random
import json
import csv
from datetime import date

def init():
    f = open("apikey", "r")
    f.readline()
    key0=f.readline().split(",")
    key1=f.readline().split(",")
    key2=f.readline().split(",")
    key3=f.readline().split(",")
    f.close()

    def getAuth(key):
        auth = tweepy.OAuthHandler(key[0], key[1])
        auth.set_access_token(key[2], key[3])
        return auth

    class Listener(tweepy.StreamListener):
        def on_data(self, data):
            par= json.loads(data)
            day=str(date.today())
            writer1 = csv.writer(open(day+'appledata.csv', 'a', newline=''))
            writer2 = csv.writer(open(day+'androiddata.csv', 'a', newline=''))
            try:
                row=[par["id"], par["created_at"],par["text"].replace("\n",""),par["user"]["followers_count"],par["in_reply_to_status_id_str"]]
                print(row[0],end="\r")
                if any (x in str(par["text"]).lower() for x in ["ipad","macbook","iphone","macbookpro","macbookair","apple"]):
                    writer1.writerow(row)
                else:
                    writer2.writerow(row)
                writer1.close()
                writer2.close()
            except:
                pass

        def error(self, status):
            print(status)

    auth=getAuth(key0)
    l = Listener()
    stream = tweepy.Stream(auth, l)
    stream.filter(track=["ipad","macbook","iphone","macbookpro","macbookair","apple","samsung","huawei","oneplus"],languages=["en"])
    return 1

while True:
    try:
        stat=init()
    except:
        time.sleep(60)