import os
import pickle
import numpy as np
from bson.objectid import ObjectId
from operator import itemgetter
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
    result = collection.find({'ticker':ticker,'volume':{ '$exists':True }}, features).sort('dateNumber', pymongo.ASCENDING)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)

def getSupportAndResistance(ticker, start, time_step):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    stocks = collection.find({'ticker':ticker},{'close':1, 'dateNumber':1, '_id':0}).sort('dateNumber', pymongo.ASCENDING)
    returns = []
    # remove first time_step counts (input based on last point)
    stocks = list(stocks)[start:]
    for stock in stocks:
        result = collection.find({
            'ticker':ticker,
            'dateNumber': {'$gt': stock['dateNumber']}
        },{'close':1, 'low':1, '_id':0}).sort('dateNumber', pymongo.ASCENDING).limit(time_step)
        startPrice = stock['close']
        if result.count(with_limit_and_skip=True) == time_step:
            result = list(result)[0:time_step]
            high = max(result, key=itemgetter('close'))['close']
            low = min(result, key=itemgetter('close'))['close']
            close = result[time_step-1]['close']
            high = (high - startPrice) / startPrice
            low = (low - startPrice) / startPrice
            close = (close - startPrice) / startPrice
            returns.append([high,low,close])
    return np.array(returns)

def get3dData(stocks, time_steps):
    length = len(stocks)
    resultData = []
    for i in range(time_steps,length-time_steps):
        datapoint = stocks[i-time_steps:i]
        resultData.append(datapoint)
    return np.array(resultData, np.float32)


def getSinglePointInput(ticker, dateNumber, features):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find_one({
        'ticker':ticker, 'dateNumber':
            { '$gte': dateNumber }
    }, features, sort=[("dateNumber", pymongo.ASCENDING)])
    resultArray = [[float(v) for v in result.values()]]
    return np.array(resultArray)

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
