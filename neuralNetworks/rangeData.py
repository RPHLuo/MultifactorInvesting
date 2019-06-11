from keras.utils import Sequence
import os
import pickle
import numpy as np
from bson.objectid import ObjectId
import pymongo
STOCKFEATURESIZE = 8
STOCKFEATURES = {'close':1, 'open':1, 'high':1, 'low':1 'volume':1, 'currentRatio':1, 'debtEquity':1, 'marketCap':1, 'pb':1, 'pe': 1, 'yd':1, '_id':0}

def size(ticker):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = self._collection.find({'ticker':ticker},STOCKFEATURES)
    return len(size)

def get(ticker, size, order):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = self._collection.find({'ticker':ticker},STOCKFEATURES).sort('dateNumber', order).limit(size)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)
def getAll(ticker):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({'ticker':ticker},STOCKFEATURES).sort('dateNumber', pymongo.ASCENDING)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)
def getAllPrices(ticker):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({'ticker':ticker},{'close':1, '_id':0}).sort('dateNumber', pymongo.ASCENDING)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)

def get3dData(stocks, time_steps):
    length = len(stocks)
    resultData = []
    for i in range(0,length-time_steps):
        datapoint = stocks[i:i+time_steps]
        resultData.append(datapoint)
    return np.array(resultData, np.float32)
