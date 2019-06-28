import os
import pickle
import numpy as np
from bson.objectid import ObjectId
import pymongo
url = 'mongodb://mongo:27017/'
try:
    test = pymongo.MongoClient(url)
    test.admin.command('ismaster')
except pymongo.errors.ConnectionFailure:
    url = 'mongodb://localhost:27017/'

def getAll(ticker, features):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({'ticker':ticker,'volume':{ '$exists':True }},features).sort('dateNumber', pymongo.ASCENDING)
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
    for i in range(time_steps,length):
        datapoint = stocks[i-time_steps:i]
        resultData.append(datapoint)
    return np.array(resultData, np.float32)

def getSingleSeqInput(ticker, dateNumber, time_step, features):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({
        'ticker':ticker, 'dateNumber':
            { '$lte': dateNumber }
        ,'volume':{ '$exists':True }}, features).sort('dateNumber', pymongo.DESCENDING).limit(time_step)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)
