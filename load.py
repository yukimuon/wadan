# This file provide the load function for further use, returns the dict containing everyday's sentiment analysis data
import pickle

def loadrec():
    with open("dayrec.pickle", "rb") as handle:
        days_rec=pickle.load(handle)
        return days_rec
