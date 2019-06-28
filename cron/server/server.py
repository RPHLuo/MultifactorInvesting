from flask import Flask, request, json, jsonify
from datetime import datetime
import os, sys
import joblib
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
@app.route('/available/stocks', methods=['GET'])
def getAvailableStocks():
    supportedStocks = open('./supportedList','r')
    tickers = supportedStocks.read().split('\n')
    tickers = tickers[0:-1]
    return jsonify(tickers)

@app.route('/predict', methods=['POST'])
def run():
    ticker = request.json['ticker']
    time_step = request.json['time_step']
    dateNumber = request.json['dateNumber']
    target_result, seq_result = weighted_target_ensemble.run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)
    return jsonify(target_result)

@app.route('/train', methods=['POST'])
def train():
    ticker = request.json['ticker'] if request.json['ticker'] else 'AEM'
    time_step = request.json['time_step'] if request.json['time_step'] else 200
    train_networks = [request.json['network']] if request.json['network'] else networks.keys()
    for n in train_networks:
        networks[n].train(ticker=ticker, time_step=time_step, start=0, epochs=10, path=path)
    return 'training'
