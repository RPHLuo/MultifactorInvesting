from datetime import datetime
import pymongo
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']
ticker = "BAM.A"
file = open('cadusd.csv', 'r')
lines = file.read().split('\n')
file.close()
data = {}
for line in lines:
    lineData = line.split(' ')
    if line != '':
        date = datetime.strptime(lineData[0].strip(), '%m/%d/%Y')
        price = float(lineData[1].strip())
        data[date] = price

stockData = stocks.find({'ticker':ticker}).sort('date')
priceData = {}
keys = sorted(data.keys())
for stock in stockData:
    date = datetime.strptime(stock['date'], '%d/%m/%Y')
    price = float(stock['adjustedPrice'])
    for index in range(1,len(keys)):
        if (date < keys[index] and date < keys[index - 1]):
            reportDate = keys[index - 1]
            price = float(data[reportDate])
            stock['pe'] *= price
            stock['pb'] *= price
            stock['yd'] /= price
            del stock['_id']
            stocks.update({ 'ticker':stock['ticker'], 'date':stock['date'] }, { '$set':stock })
            break
        elif len(keys) == index + 1:
            reportDate = keys[index]
            price = float(data[reportDate])
            stock['pe'] *= price
            stock['pb'] *= price
            stock['yd'] /= price
            stock['marketCap'] *= price
            del stock['_id']
            stocks.update({ 'ticker':stock['ticker'], 'date':stock['date'] }, { '$set':stock })
