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
        volumeText = str(stock['volume'])
        volume = 0

        if 'k' in volumeText:
            volume = float(volumeText.replace('k',''))
            volume *= 1000
        elif 'm' in volumeText:
            volume = float(volumeText.replace('m',''))
            volume *= 1000000
        else:
            volume = float(volumeText)
        stock['volume'] = volume
        stock['close'] = float(stock['close'].replace(',',''))
        stock['low'] = float(stock['low'].replace(',',''))
        stock['open'] = float(stock['open'].replace(',',''))
        del stock['_id']
        stocks.update({'ticker':ticker,'date':stock['date']}, {'$set':stock})
