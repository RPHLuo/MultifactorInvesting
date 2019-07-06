from datetime import datetime
import pymongo
mongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
tsx60data = mongoClient['tsx60data']
stocks = tsx60data['stocks']
ticker = 'BAM.A'
filePath = 'SP/'+ ticker
file = open(filePath, 'r')
lines = file.read().split('\n')
file.close()
for line in lines:
    if line != '':
        data = line.split('\t')
        dateText = data[0].split(' ')[0]
        date = datetime.strptime(dateText, '%m/%d/%Y').strftime('%d/%m/%Y')
        dateNumber = int(datetime.strptime(date, '%d/%m/%Y').strftime('%Y%m%d'))
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
            'volume':volume,
            'dateNumber':dateNumber
        }
        stocks.update({'ticker':ticker,'date':date},{ '$set':stock }, upsert=True)
