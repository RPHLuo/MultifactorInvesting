from datetime import datetime
import pymongo
mongoClient = pymongo.MongoClient("mongodb://mongo:27017/")
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']
tickers = constituents.find()
missing = stocks.find({'debtEquity':{ '$exists': False }})
for m_stock in missing:
    last_stock = stocks.find_one({
        'ticker':m_stock['ticker'],
        'debtEquity': { '$exists':True },
        'currentRatio': { '$exists':True },
        'dateNumber': { '$lte': m_stock['dateNumber'] }
    }, sort=[("dateNumber", pymongo.DESCENDING)])
    if not hasattr(m_stock,'debtEquity'):
    m_stock['debtEquity'] = last_stock['debtEquity']
    if not hasattr(m_stock,'currentRatio'):
    m_stock['currentRatio'] = last_stock['currentRatio']
    del m_stock['_id']
    stocks.update({'ticker':m_stock['ticker'],'date':m_stock['date']}, {'$set':m_stock})
