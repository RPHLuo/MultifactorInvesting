from flask import Flask, request, jsonify
import json
from jsonpickle import pickler
from datetime import datetime, timedelta
import os, sys
import joblib
import stock_data
path = '../neuralNetworks/'
lib_path = os.path.abspath(os.path.join(path))
sys.path.append(lib_path)
import weighted_target_ensemble
import seq_fundamental_lstm, seq_technical_lstm, seq_fundamental_cnn, seq_technical_cnn
import target_fundamental_ffnn, target_technical_cnn, target_fundamental_lstm
app = Flask(__name__)
networks = {
    'seq_fundamental_lstm':seq_fundamental_lstm,
    'seq_technical_lstm':seq_technical_lstm,
    'seq_fundamental_cnn':seq_fundamental_cnn,
    'seq_technical_cnn':seq_technical_cnn,
    'target_fundamental_ffnn':target_fundamental_ffnn,
    'target_technical_cnn':target_technical_cnn,
    'target_fundamental_lstm':target_fundamental_lstm
}

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

@app.route('/available/stocks', methods=['GET'])
def getAvailableStocks():
    supportedStocks = open('./supportedList','r')
    tickers = supportedStocks.read().split('\n')
    tickers = tickers[0:-1]
    return jsonify(tickers)

#@app.route('/predict_old', methods=['POST'])
#def predict_old():
#    jpickle = pickler.Pickler()
#    ticker = request.json['ticker']
#    time_step = request.json['time_step']
#    dateNumber = request.json['dateNumber']
#    target_result, seq_result = weighted_target_ensemble.run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)
#    date = datetime.strptime(str(dateNumber), '%Y%m%d')
#    dateData = nextDates(date, time_step)
#    seq_result = list(seq_result)
#    seq_result = [{'predict':str(seq_result[i]),'date':dateData[i]} for i in range(0,time_step)]
#    print(seq_result)
#    return json.dumps({ 'sequence':seq_result, 'target':list(target_result) })


@app.route('/predict', methods=['POST'])
def predict():
    ticker = request.json['ticker']
    time_step = request.json['time_step']
    dateNumber = request.json['dateNumber']
    result = predictions.find_one({'ticker':ticker, 'dateNumber': dateNumber, 'time_step':time_step})
    if result:
        del result['_id']
        return json.dumps(result)
    else:
        return 'does not exist'

@app.route('/quote', methods=['POST'])
def quote():
    ticker = request.json['ticker']
    start = request.json['start'] if request.json['start'] else 0
    prices = stock_data.getAllPrices(ticker, start)
    return jsonify(prices)

@app.route('/predict/single', methods=['POST'])
def predict_single():
    ticker = request.json['ticker']
    time_step = request.json['time_step']
    dateNumber = request.json['dateNumber']
    network = request.json['network']
    result = networks[n].run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)
    result = result.flatten()
    return jsonify(list(result))

@app.route('/train', methods=['POST'])
def train():
    ticker = request.json['ticker'] if request.json['ticker'] else 'AEM'
    time_step = request.json['time_step'] if request.json['time_step'] else 200
    train_networks = [request.json['network']] if request.json['network'] else networks.keys()
    for n in train_networks:
        networks[n].train(ticker=ticker, time_step=time_step, start=0, epochs=10, path=path)
    return 'training'
