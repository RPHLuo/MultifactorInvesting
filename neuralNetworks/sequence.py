from keras.utils import Sequence
import os
import pickle
import numpy as np
from bson.objectid import ObjectId
import pymongo
STOCKFEATURESIZE = 8
STOCKFEATURES = {'close':1, 'volume':1, 'currentRatio':1, 'debtEquity':1, 'marketCap':1, 'pb':1, 'pe': 1, 'yd':1, '_id':0}
class MongoSequence(Sequence):
    def __init__(self, dataset_size, batch_size, query=None, server='mongodb://localhost:27017/', database="tsx60data", collection="stocks"):
        self._server = server
        self._db = database
        self._collection_name = collection
        self._batch_size = batch_size
        self._query = query
        self._dataset_size = dataset_size
        self._collection = self._connect()
        result = self._collection.find(self._query, {'_id': True}).sort('dateNumber', pymongo.ASCENDING).limit(self._dataset_size)
        self._object_ids = [ stock['_id'] for stock in result ]

        self._pid = os.getpid()
        del self._collection   #  to be sure, that we've disconnected
        self._collection = None

    def _connect(self):
        client = pymongo.MongoClient(self._server)
        db = client[self._db]
        return db[self._collection_name]

    def __len__(self):
        return int(np.ceil(len(self._object_ids) / float(self._batch_size)))

    def __getitem__(self, index):
        if self._collection is None or self._pid != os.getpid():
            self._collection = self._connect()
            self._pid = os.getpid()

        oids = self._object_ids[index * self._batch_size: (index+1) * self._batch_size]
        X = np.empty((len(oids), STOCKFEATURESIZE), dtype=np.float32)
        for i, oid in enumerate(oids):
            stock = self._connect().find_one({'_id': oid},STOCKFEATURES)
            X[i] = np.array([ v for v in stock.values() ]).astype(np.float32)
        return X

def size(ticker):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = self._collection.find({'ticker':ticker,'volume':{ '$exists':True }},STOCKFEATURES)
    return len(size)

def get(ticker, size, order):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = self._collection.find({'ticker':ticker,'volume':{ '$exists':True }},STOCKFEATURES).sort('dateNumber', order).limit(size)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)
def getAll(ticker):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({'ticker':ticker,'volume':{ '$exists':True }},STOCKFEATURES).sort('dateNumber', pymongo.ASCENDING)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)
def getAllPrices(ticker):
    client = pymongo.MongoClient('mongodb://localhost:27017/')
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
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['tsx60data']
    collection = db['stocks']
    result = collection.find({
        'ticker':ticker, 'dateNumber':
            { '$gte': dateNumber }
        ,'volume':{ '$exists':True }}, STOCKFEATURES).sort('dateNumber', pymongo.ASCENDING).limit(time_step)
    resultArray = [[float(v) for v in stock.values()] for stock in result ]
    return np.array(resultArray)
