import os, sys
path = './neuralNetworks/'
lib_path = os.path.abspath(os.path.join(path))
sys.path.append(lib_path)
import json
import weighted_target_ensemble
from datetime import datetime, timedelta
import pymongo
url = 'mongodb://mongo:27017/'
try:
    test = pymongo.MongoClient(url)
    test.admin.command('ismaster')
except pymongo.errors.ConnectionFailure:
    url = 'mongodb://localhost:27017/'

mongoClient = pymongo.MongoClient(url)
tsx60data = mongoClient['tsx60data']
predictions = tsx60data['predict']
stocks = tsx60data['stocks']

supportedStocks = open('./supportedList','r')
tickers = supportedStocks.read().split('\n')
tickers = tickers[0:-1]
time_steps=[20,50,100,200]

def nextDates(date, time_step):
    result = []
    while len(result) != 200:
        date += timedelta(days=1)
        day = date.weekday()
        if day < 5:
            result.append(date.strftime('%d/%m/%Y'))
    return result

latest = stocks.find_one({}, sort=[("dateNumber", pymongo.DESCENDING)])
date_number = latest['dateNumber']

for ticker in tickers:
    for time_step in time_steps:
        date_number = 20190531
        target_result, seq_result = weighted_target_ensemble.run(ticker=ticker, dateNumber=date_number, time_step=time_step, path=path)
        date = datetime.strptime(str(date_number), '%Y%m%d')
        date_data = nextDates(date, time_step)
        seq_result = [{'close':str(seq_result[i]), 'date':date_data[i]} for i in range(0,time_step)]
        target_result = [str(result) for result in target_result]
        predictions.update({ 'ticker':ticker, 'time_step':time_step, 'dateNumber':date_number }, {
            'ticker':ticker,
            'seq_result':json.dumps(seq_result),
            'target_result':json.dumps(target_result),
            'dateNumber':date_number,
            'time_step':time_step
        }, upsert=True)
