from keras.layers import Input, LSTM, Dropout, Dense
from keras.models import Model, Sequential
from sklearn.preprocessing import MinMaxScaler
import lstm_data
import numpy as np
import pymongo
from matplotlib import pyplot
import math
import os
from sklearn.externals import joblib

def train(ticker='AEM', time_step=200, start=0, epochs=10, path='./'):
    inputset = lstm_data.getAll(ticker)
    outputset = lstm_data.getAllPrices(ticker)

    scaler_filename = path + 'scalers/' + ticker+'_lstm_input.scaler'
    price_scaler_filename = path + 'scalers/' + ticker+'_lstm_output.scaler'
    file = path + 'weights/' + ticker + '_lstm_' + str(time_step) + '_steps.h5'

    scaler = MinMaxScaler(feature_range=(0, 1))
    price_scaler = MinMaxScaler(feature_range=(0, 1))
    if os.path.exists(scaler_filename):
        scaler = joblib.load(scaler_filename)
        inputset = scaler.transform(inputset)
    else:
        inputset = scaler.fit_transform(inputset)
        file_writer = open(scaler_filename,'w+')
        file_writer.close()
        joblib.dump(scaler, scaler_filename)

    if os.path.exists(price_scaler_filename):
        price_scaler = joblib.load(price_scaler_filename)
        outputset = price_scaler.transform(outputset)
    else:
        outputset = price_scaler.fit_transform(outputset)
        file_writer = open(price_scaler_filename,'w+')
        file_writer.close()
        joblib.dump(price_scaler, price_scaler_filename)

    inputset = lstm_data.get3dData(inputset, time_step)
    dataset_size = len(inputset)
    train_percent = 0.7

    train_size = math.floor(train_percent * dataset_size)
    test_size = dataset_size - train_size
    predict_length=1

    train_X = inputset[start:train_size]
    test_X = inputset[train_size:]
    train_y = outputset[start+time_step:train_size+time_step]
    test_y = outputset[train_size+time_step:]

    model = Sequential()
    model.add(LSTM(200, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mae')

    if os.path.exists(file):
        model.load_weights(file)
    history = model.fit(train_X, train_y, epochs=epochs, batch_size=30, validation_data=(test_X, test_y), verbose=2, shuffle=False)
    #save weights
    model.save_weights(file)

def run(ticker='AEM', dateNumber=20180608, time_step=200, path='./'):
    scaler_filename = path + 'scalers/' + ticker+'_lstm_input.scaler'
    price_scaler_filename = path + 'scalers/' + ticker+'_lstm_output.scaler'
    file = path + 'weights/' + ticker + '_lstm_' + str(time_step) + '_steps.h5'

    scaler = MinMaxScaler(feature_range=(0, 1))
    price_scaler = MinMaxScaler(feature_range=(0, 1))

    inputset = lstm_data.getAll(ticker)
    outputset = lstm_data.getAllPrices(ticker)

    if os.path.exists(scaler_filename):
        scaler = joblib.load(scaler_filename)
    else:
        inputset = scaler.fit_transform(inputset)
        file_writer = open(scaler_filename,'w+')
        file_writer.close()
        joblib.dump(scaler, scaler_filename)

    if os.path.exists(price_scaler_filename):
        price_scaler = joblib.load(price_scaler_filename)
    else:
        price_scaler.fit_transform(outputset)
        file_writer = open(price_scaler_filename,'w+')
        file_writer.close()
        joblib.dump(price_scaler, price_scaler_filename)

    stockdata = lstm_data.getSinglePointInput(ticker, dateNumber, time_step+1)
    stockdata = scaler.transform(stockdata)
    stockdata = lstm_data.get3dData(stockdata, time_step)

    model = Sequential()
    model.add(LSTM(200, input_shape=(stockdata.shape[1], stockdata.shape[2])))
    model.add(Dense(1))

    if os.path.exists(file):
        model.load_weights(file)
        model.compile(optimizer='adam', loss='mae')
        prediction = model.predict(stockdata)
        prediction = price_scaler.inverse_transform(prediction)
        print(prediction)
        return prediction

#old dev code
#predict_here, change time_step to current (-1)
#input = np.array([inputset[-time_step,:]])
#prediction = model.predict(input)
#prediction = priceScaler.inverse_transform(prediction)
#print(prediction)

# plot history
#pyplot.plot(history.history['loss'], label='train')
#pyplot.plot(history.history['val_loss'], label='test')
#pyplot.legend()
#pyplot.show()
