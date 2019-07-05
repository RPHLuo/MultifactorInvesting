from datetime import datetime
import pymongo
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']
constituents = tsx60data['constituents']
earnings = tsx60data['earnings']
ticker = "BAM.A"
file = open(ticker+'.csv', 'r')
lines = file.read().split('\n')
lines.pop(0)
file.close()
data = {}
for line in lines:
    lineData = line.split(',')
    if line != '':
        date = datetime.strptime(lineData[0].strip(), '%d/%m/%Y')
        sharesOutstanding = float(lineData[1].strip())
        dividend = float(lineData[2].strip())
        debtEquity = float(lineData[4].strip())
        currentRatio = float(lineData[3].strip())
        eps = float(lineData[6].strip())
        bookValue = float(lineData[5].strip())
        data[date] = {
            'sharesOutstanding':sharesOutstanding,
            'dividend':dividend,
            'debtEquity':debtEquity,
            'currentRatio':currentRatio,
            'eps':eps,
            'bookValue':bookValue
        }
stockData = stocks.find({'ticker':ticker}).sort('date')
priceData = {}
keys = sorted(data.keys())
for stock in stockData:
    date = datetime.strptime(stock['date'], '%d/%m/%Y')
    price = float(stock['adjustedPrice'])
    for index in range(1,len(keys)):
        if (date < keys[index] and date < keys[index - 1]):
            reportDate = keys[index - 1]
            report = data[reportDate]
            stock['pe'] = price / report['eps']
            stock['pb'] = price / report['bookValue']
            stock['yd'] = report['dividend'] / price
            stock['marketCap'] = price * report['sharesOutstanding']
            stock['debtEquity']  = report['debtEquity']
            stock['currentRatio'] = report['currentRatio']
            del stock['_id']
            stocks.update({ 'ticker':stock['ticker'], 'date':stock['date'] }, { '$set':stock })
            break
        elif len(keys) == index + 1:
            reportDate = keys[index]
            report = data[reportDate]
            stock['pe'] = price / report['eps']
            stock['pb'] = price / report['bookValue']
            stock['yd'] = report['dividend'] / price
            stock['marketCap'] = price * report['sharesOutstanding']
            stock['debtEquity']  = report['debtEquity']
            stock['currentRatio'] = report['currentRatio']
            del stock['_id']
            stocks.update({ 'ticker':stock['ticker'], 'date':stock['date'] }, { '$set':stock })
