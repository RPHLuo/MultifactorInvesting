from keras.layers import Dropout, Dense, Conv1D, Conv2D, MaxPooling1D, Flatten
from keras.models import Model, Sequential
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import cnn_data
import numpy as np
import pymongo
from matplotlib import pyplot
import math
import os
import joblib

def train(ticker='AEM', time_step=200, start=0, epochs=10, path='./'):
    inputset = cnn_data.getAll(ticker)
    outputset = cnn_data.getSupportAndResistance(ticker, time_step)

    print(inputset.shape)
    print(outputset.shape)

    scaler_filename = path + 'scalers/' + ticker+'_cnn_input.scaler'
    price_scaler_filename = path + 'scalers/' + ticker+'_cnn_output.scaler'
    file = path + 'weights/' + ticker + '_cnn_' + str(time_step) + '_steps.h5'

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

    inputset = cnn_data.get3dData(inputset, time_step)
    dataset_size = len(inputset)
    test_size = 0.3

    train_X, test_X, train_y, test_y = train_test_split(inputset, outputset, test_size=test_size)

    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=200, input_shape=(train_X.shape[1], train_X.shape[2])))
    model.add(MaxPooling1D(pool_size=1))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(3))

    model.compile(optimizer='adam', loss='mse')

    if os.path.exists(file):
        model.load_weights(file)
    history = model.fit(train_X, train_y, epochs=epochs, batch_size=30, validation_data=(test_X, test_y), verbose=2, shuffle=False)
    # save weights
    model.save_weights(file)

def run(ticker='AEM', dateNumber=20180608, time_step=200, path='./'):
    scaler_filename = path + 'scalers/' + ticker+'_cnn_input.scaler'
    price_scaler_filename = path + 'scalers/' + ticker+'_cnn_output.scaler'
    file = path + 'weights/' + ticker + '_cnn_' + str(time_step) + '_steps.h5'

    scaler = MinMaxScaler(feature_range=(0, 1))
    price_scaler = MinMaxScaler(feature_range=(0, 1))

    inputset = cnn_data.getAll(ticker)
    outputset = cnn_data.getSupportAndResistance(ticker, time_step)

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

    stockdata = cnn_data.getSinglePointInput(ticker, dateNumber, time_step+1)
    stockdata = scaler.transform(stockdata)
    stockdata = cnn_data.get3dData(stockdata, time_step)

    model = Sequential()
    model.add(Conv1D(filters=64, kernel_size=200, input_shape=(stockdata.shape[1], stockdata.shape[2])))
    model.add(MaxPooling1D(pool_size=1))
    model.add(Flatten())
    model.add(Dense(50, activation='relu'))
    model.add(Dense(3))

    if os.path.exists(file):
        model.load_weights(file)
        model.compile(optimizer='adam', loss='mse')
        prediction = model.predict(stockdata)
        prediction = price_scaler.inverse_transform(prediction)
        print(stockdata[-1][-1])
        print(prediction)
        return prediction
