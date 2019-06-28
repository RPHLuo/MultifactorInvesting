from keras.layers import Input, Dropout, Dense
from keras.models import Model, Sequential
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import target_data
import numpy as np
import pymongo
from matplotlib import pyplot
import math
import os
import joblib
STOCKFEATURES = {'currentRatio':1, 'debtEquity':1, 'marketCap':1, 'pb':1, 'pe': 1, 'yd':1, '_id':0}
model_id = 'target_fundamental_ffnn'
def train(ticker='AEM', time_step=200, start=0, epochs=10, path='./'):
    inputset = target_data.getAll(ticker, STOCKFEATURES)
    outputset = target_data.getSupportAndResistance(ticker, 0, time_step)

    scaler_filename = path + 'scalers/' + ticker+'_' + model_id + '_input.scaler'
    price_scaler_filename = path + 'scalers/' + ticker + '_' + model_id + '_output.scaler'
    file = path + 'weights/' + ticker + '_' + model_id + '_' + str(time_step) + '_steps.h5'

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

    test_size = 0.3
    inputset = inputset[start:-time_step]
    outputset = outputset[start:]
    train_X, test_X, train_y, test_y = train_test_split(inputset, outputset, test_size=test_size)

    #architecture
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(train_X.shape[1],)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(3, activation='sigmoid'))
    model.compile(optimizer='sgd', loss='mean_squared_error')

    if os.path.exists(file):
        model.load_weights(file)
    history = model.fit(train_X, train_y, epochs=epochs, batch_size=32, validation_data=(test_X, test_y), verbose=2, shuffle=False)
    model.save_weights(file)

def run(ticker='AEM', dateNumber=20180608, time_step=200, path='./'):
    scaler_filename = path + 'scalers/' + ticker+'_' + model_id + '_input.scaler'
    price_scaler_filename = path + 'scalers/' + ticker + '_' + model_id + '_output.scaler'
    file = path + 'weights/' + ticker + '_' + model_id + '_' + str(time_step) + '_steps.h5'

    scaler = MinMaxScaler(feature_range=(0, 1))
    price_scaler = MinMaxScaler(feature_range=(0, 1))

    inputset = target_data.getAll(ticker, STOCKFEATURES)
    outputset = target_data.getSupportAndResistance(ticker, 0, time_step)

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

    stockdata = target_data.getSinglePointInput(ticker, dateNumber, STOCKFEATURES)
    stockdata = scaler.transform(stockdata)

    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=(stockdata.shape[1],)))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(3, activation='sigmoid'))

    if os.path.exists(file):
        model.load_weights(file)
        model.compile(optimizer='sgd', loss='mean_squared_error')
        prediction = model.predict(stockdata)
        prediction = price_scaler.inverse_transform(prediction)
        return prediction

#predict_here, change time_step to current (-1)
#input = np.array([inputset[-time_step,:]])
#prediction = model.predict(input)
#prediction = price_scaler.inverse_transform(prediction)
#print(prediction)
# plot history
#pyplot.plot(history.history['loss'], label='train')
#pyplot.plot(history.history['val_loss'], label='test')
#pyplot.legend()
#pyplot.show()
