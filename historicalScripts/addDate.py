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
        dateText = stock['date']
        date = datetime.strptime(dateText, '%d/%m/%Y').strftime('%Y%m%d')
        stock['dateNumber'] = int(date)
        del stock['_id']
        stocks.update({'ticker':ticker,'date':dateText}, {'$set':stock})
