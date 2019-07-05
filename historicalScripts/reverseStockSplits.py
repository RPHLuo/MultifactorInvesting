from datetime import datetime
import pymongo
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']
constituents = tsx60data['constituents']
ticker = "BAM.A"
#dateNumber
splitDates = [20040602,20060428,20070604,20150512]
#1 share = how many shares
splitRatios = [1.5, 1.5, 1.5, 1.5]
for i in range(0,splitDates):
	data = stocks.find({'ticker':ticker, 'dateNumber':{ '$lt':splitDates[i] }})
	for stock in data:
		if not stock['adjustedPrice']:
			stock['adjustedPrice'] = stock['close']
		stock['adjustedPrice'] *= splitRatios[i]
	    del stock['_id']
	    stocks.update({'ticker':ticker,'date':stock['date']}, {'$set':stock})
