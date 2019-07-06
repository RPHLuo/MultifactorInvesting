from datetime import datetime
import pymongo
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']
constituents = tsx60data['constituents']
tickers = constituents.find()
for t in tickers:
    ticker = t['ticker']
    data = stocks.find({'ticker':ticker})
    for stock in data:
    	if not 'adjustedPrice' in stock:
    		stock['adjustedPrice'] = stock['close']
            del stock['_id']
            stocks.update({'ticker':ticker,'date':stock['date']}, {'$set':stock})
