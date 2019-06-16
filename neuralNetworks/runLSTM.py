from keras.layers import Input, LSTM, Dense
from keras.models import Model, Sequential
from sklearn.preprocessing import MinMaxScaler
import lstm_data
import numpy as np
import pymongo
from matplotlib import pyplot
import math
import os
time_step = 200
dateNumber = 20180608
ticker = 'AEM'

#scaler
dataset = lstm_data.getAll(ticker)
outputset = lstm_data.getAllPrices(ticker)
scaler = MinMaxScaler(feature_range=(0, 1))
priceScaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(dataset)
outputset = priceScaler.fit_transform(outputset)

stockdata = lstm_data.getSinglePointInput(ticker, dateNumber, time_step+1)
stockdata = scaler.transform(stockdata)
stockdata = lstm_data.get3dData(stockdata, time_step)

model = Sequential()
model.add(LSTM(200, input_shape=(stockdata.shape[1], stockdata.shape[2])))
model.add(Dense(1))

if os.path.exists('aem_lstm_weights.h5'):
    model.load_weights('aem_lstm_weights.h5')
    model.compile(optimizer='adam', loss='mae')
    prediction = model.predict(stockdata)
    prediction = priceScaler.inverse_transform(prediction)
    print(prediction)
