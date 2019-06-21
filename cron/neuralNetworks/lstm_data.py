import os
import pickle
import numpy as np
from bson.objectid import ObjectId
import pymongo
STOCKFEATURESIZE = 8
STOCKFEATURES = {'close':1, 'volume':1, 'currentRatio':1, 'debtEquity':1, 'marketCap':1, 'pb':1, 'pe': 1, 'yd':1, '_id':0}
url = 'mongodb://mongo:27017/'
def size(ticker):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    result = self._collection.find({'ticker':ticker,'volume':{ '$exists':True }},STOCKFEATURES)
    return len(size)

def get(ticker, size, order):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    result = self._collection.find({'ticker':ticker,'volume':{ '$exists':True }},STOCKFEATURES).sort('dateNumber', order).limit(size)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)
def getAll(ticker):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({'ticker':ticker,'volume':{ '$exists':True }},STOCKFEATURES).sort('dateNumber', pymongo.ASCENDING)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)
def getAllPrices(ticker):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({'ticker':ticker,'volume':{ '$exists':True }},{'close':1, '_id':0}).sort('dateNumber', pymongo.ASCENDING)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)

def get3dData(stocks, time_steps):
    length = len(stocks)
    resultData = []
    for i in range(0,length-time_steps):
        datapoint = stocks[i:i+time_steps]
        resultData.append(datapoint)
    return np.array(resultData, np.float32)

def getSinglePointInput(ticker, dateNumber, time_step):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({
        'ticker':ticker, 'dateNumber':
            { '$gte': dateNumber }
        ,'volume':{ '$exists':True }}, STOCKFEATURES).sort('dateNumber', pymongo.ASCENDING).limit(time_step)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)
