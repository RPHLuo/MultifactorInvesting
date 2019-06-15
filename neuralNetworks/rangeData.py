from keras.utils import Sequence
import os
import pickle
import numpy as np
from bson.objectid import ObjectId
import pymongo
from operator import itemgetter
STOCKFEATURESIZE = 8
STOCKFEATURES = {'currentRatio':1, 'debtEquity':1, 'marketCap':1, 'pb':1, 'pe': 1, 'yd':1, '_id':0}

def size(ticker):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = self._collection.find({'ticker':ticker},STOCKFEATURES)
    return len(size)
def getAll(ticker):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({'ticker':ticker},STOCKFEATURES).sort('dateNumber', pymongo.ASCENDING)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)

#find the potential gain and potential loss at the end of this period
def getBestPrices(ticker, stocks, length):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    stocks = collection.find({'ticker':ticker},{'close':1, 'dateNumber':1, '_id':0}).sort('dateNumber', pymongo.ASCENDING)
    returns = []
    for stock in stocks:
        result = collection.find({
            'ticker':ticker,
            'dateNumber': {'$gt': stock['dateNumber']}
        },{'close':1, 'low':1, '_id':0}).sort('dateNumber', pymongo.ASCENDING).limit(length)
        startPrice = stock['close']
        if result.count(with_limit_and_skip=True) == length:
            result = list(result)[0:length]
            high = max(result, key=itemgetter('close'))['close']
            low = min(result, key=itemgetter('low'))['low']
            close = result[length-1]['close']
            high = (high - startPrice) / startPrice
            low = (low - startPrice) / startPrice
            close = (close - startPrice) / startPrice
            returns.append([high,low,close])
    return np.array(returns)
