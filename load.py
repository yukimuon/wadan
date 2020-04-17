import pickle

with open("dayrec.pickle", "rb") as handle:
    dayrec=pickle.load(handle)
    print(dayrec)
