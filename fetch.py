#! /usr/bin/python3

import time
import tweepy
import pickle
import random
import json
import csv

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
            # print(par)
            try:
                row=[par["id"], par["created_at"],par["text"].replace("\n",""),par["user"]["followers_count"],par["in_reply_to_status_id_str"]]
                print(row)
                writer.writerow(row)
            except:
                pass

        def error(self, status):
            print(status)

    auth=getAuth(key0)
    writer = csv.writer(open('data.csv', 'a', newline=''))
    l = Listener()
    stream = tweepy.Stream(auth, l)
    stream.filter(track=["zcash","monero","bitcoin"])
    return 1

while True:
    stat=init()
    time.sleep(60)