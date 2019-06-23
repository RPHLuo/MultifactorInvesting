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
        lastStock = stocks.find_one({
                'ticker':ticker,
                'debtEquity': { '$exists':True },
                'currentRatio': { '$exists':True },
                'dateNumber':
                    { '$lte': stock['dateNumber'] }
            }, sort=[("dateNumber", pymongo.DESCENDING)])
        if (not hasattr(stock,'debtEquity')):
            stock['debtEquity'] = lastStock['debtEquity']
        if (not hasattr(stock,'currentRatio')):
            stock['currentRatio'] = lastStock['currentRatio']

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
        stock['close'] = float(str(stock['close']).replace(',',''))
        stock['low'] = float(str(stock['low']).replace(',',''))
        stock['open'] = float(str(stock['open']).replace(',',''))
        del stock['_id']
        stocks.update({'ticker':ticker,'date':stock['date']}, {'$set':stock})
