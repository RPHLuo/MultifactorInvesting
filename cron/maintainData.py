from datetime import datetime
import pymongo
url = 'mongodb://mongo:27017/'
try:
    test = pymongo.MongoClient(url)
    test.admin.command('ismaster')
except pymongo.errors.ConnectionFailure:
    url = 'mongodb://localhost:27017/'
mongoClient = pymongo.MongoClient(url)
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']

supportedStocks = open('./supportedList','r')
tickers = supportedStocks.read().split('\n')
tickers = tickers[0:-1]

missing = stocks.find({'ticker':{ '$in':tickers },'debtEquity':{ '$exists': False }})
for m_stock in missing:
    last_stock = stocks.find_one({
        'ticker':m_stock['ticker'],
        'debtEquity': { '$exists':True },
        'currentRatio': { '$exists':True },
        'dateNumber': { '$lte': m_stock['dateNumber'] }
    }, sort=[("dateNumber", pymongo.DESCENDING)])
    print(last_stock)
    if not hasattr(m_stock,'debtEquity'):
        m_stock['debtEquity'] = last_stock['debtEquity']
    if not hasattr(m_stock,'currentRatio'):
        m_stock['currentRatio'] = last_stock['currentRatio']
    del m_stock['_id']
    stocks.update({'ticker':m_stock['ticker'],'date':m_stock['date']}, {'$set':m_stock})
