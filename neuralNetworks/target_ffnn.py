from keras.layers import Input, Dropout, Dense
from keras.models import Model, Sequential
from sklearn.preprocessing import MinMaxScaler
import ffnn_data
import numpy as np
import pymongo
from matplotlib import pyplot
import math
import os
from sklearn.externals import joblib

def train(ticker='AEM', performance_indicator=200, start=0):
    inputset = ffnn_data.getAll(ticker)
    outputset = ffnn_data.getBestPrices(ticker, dataset, performance_indicator)

    scaler_filename = './scalers/' + ticker+'_ffnn_input.scaler'
    price_scaler_filename = './scalers/' + ticker+'_ffnn_output.scaler'
    file = './weights/' + ticker + '_ffnn_' + performance_indicator + '_steps.h5'

    scaler = MinMaxScaler(feature_range=(0, 1))
    price_scaler = MinMaxScaler(feature_range=(0, 1))
    if os.path.exists(scaler_filename):
        scaler = joblib.load(scaler_filename)
        inputset = scaler.transform(inputset)
    else:
        inputset = scaler.fit_transform(inputset)
        joblib.dump(scaler, scaler_filename)

    if os.path.exists(price_scaler_filename):
        price_scaler = joblib.load(price_scaler_filename)
        outputset = price_scaler.transform(outputset)
    else:
        outputset = price_scaler.fit_transform(outputset)
        joblib.dump(price_scaler, price_scaler_filename)

    dataset_size = len(inputset)
    train_percent = 0.7
    train_size = math.floor(train_percent * dataset_size)
    test_size = dataset_size - train_size
    train_X = inputset[start:train_size]
    test_X = inputset[train_size:-performance_indicator]
    train_y = outputset[start:train_size]
    test_y = outputset[train_size:]

    #architecture
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(train_X.shape[1],)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(3, activation='sigmoid'))
    model.compile(optimizer='sgd', loss='mean_squared_error')

    if os.path.exists(file):
        model.load_weights(file)
    history = model.fit(train_X, train_y, epochs=100, batch_size=32, validation_data=(test_X, test_y), verbose=2, shuffle=False)
    model.save_weights(file)

def run(ticker='AEM', dateNumber=20180608, time_step=200):
    scaler_filename = './scalers/' + ticker+'_ffnn_input.scaler'
    price_scaler_filename = './scalers/' + ticker+'_ffnn_output.scaler'
    file = './weights/' + ticker + '_ffnn_' + time_step + '_steps.h5'

    scaler = MinMaxScaler(feature_range=(0, 1))
    price_scaler = MinMaxScaler(feature_range=(0, 1))

    inputset = ffnn_data.getAll(ticker)
    outputset = ffnn_data.getAllPrices(ticker)

    if os.path.exists(scaler_filename):
        scaler = joblib.load(scaler_filename)
    else:
        inputset = scaler.fit_transform(inputset)
        joblib.dump(scaler, scaler_filename)
    if os.path.exists(price_scaler_filename):
        price_scaler = joblib.load(price_scaler_filename)
    else:
        price_scaler.fit_transform(outputset)
        joblib.dump(price_scaler, price_scaler_filename)

    stockdata = ffnn_data.getSinglePointInput(ticker, dateNumber)
    stockdata = scaler.transform(stockdata)

    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(train_X.shape[1],)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(3, activation='sigmoid'))

    if os.path.exists(file):
        model.load_weights(file)
        model.compile(optimizer='sgd', loss='mean_squared_error')
        prediction = model.predict(stockdata)
        prediction = price_scaler.inverse_transform(prediction)
        print(prediction)
        return prediction

#predict_here, change performance_indicator to current (-1)
#input = np.array([inputset[-performance_indicator,:]])
#prediction = model.predict(input)
#prediction = price_scaler.inverse_transform(prediction)
#print(prediction)
# plot history
#pyplot.plot(history.history['loss'], label='train')
#pyplot.plot(history.history['val_loss'], label='test')
#pyplot.legend()
#pyplot.show()
