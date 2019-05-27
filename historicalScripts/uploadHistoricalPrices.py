from datetime import datetime
import pymongo
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']
constituents = tsx60data['constituents']
tickers = constituents.find()
for t in tickers:
    ticker = t['ticker']
    print(ticker)
    filePath = 'SP/'+ ticker
    file = open(filePath, 'r')
    lines = file.read().split('\n')
    file.close()
    for line in lines:
        if line != '':
            data = line.split('\t')
            dateText = data[0].split(' ')[0]
            date = datetime.strptime(dateText, '%d/%m/%Y').strftime('%d/%m/%Y')
            openPrice = float(data[1])
            high = float(data[2])
            low = float(data[3])
            close = float(data[4])
            volume = int(data[5])
            stock = {
                'ticker':ticker,
                'date':date,
                'open':openPrice,
                'low':low,
                'close':close,
                'volume':volume
            }
            stocks.update({'ticker':ticker,'date':date},{ '$set':stock }, upsert=True)
