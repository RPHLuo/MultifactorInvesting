import os
import pickle
from bson.objectid import ObjectId
import pymongo
url = 'mongodb://mongo:27017/'
try:
    test = pymongo.MongoClient(url)
    test.admin.command('ismaster')
except pymongo.errors.ConnectionFailure:
    url = 'mongodb://localhost:27017/'

def getAllPrices(ticker, start):
    client = pymongo.MongoClient(url)
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({'ticker':ticker, 'dateNumber':{'$gte':start}},{'close':1, 'date':1, '_id':0}).sort('dateNumber', pymongo.ASCENDING)
    result = list(result)
    return result
