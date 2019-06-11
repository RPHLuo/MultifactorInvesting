from datetime import datetime
import pymongo
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']
constituents = tsx60data['constituents']
ticker = "AEM"
#dateNumber
splitDates = []
#1 share = how many shares
splitRatios = []
for i in range(0,splitDates):
	data = stocks.find({'ticker':ticker, 'dateNumber':{ '$gte':splitDates[i] }})
	for stock in data:
		if not stock['adjustedPrice']:
			stock['adjustedPrice'] = stock['close']
		stock['close'] *= splitRatios[i]
	    del stock['_id']
	    stocks.update({'ticker':ticker,'date':stock['date']}, {'$set':stock})
