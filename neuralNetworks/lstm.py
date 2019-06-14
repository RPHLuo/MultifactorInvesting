from keras.layers import Input, LSTM, Dropout, Dense
from keras.models import Model, Sequential
from sequence import MongoSequence
from sklearn.preprocessing import MinMaxScaler
import sequence
import numpy as np
import pymongo
from matplotlib import pyplot
import math
import os

ticker='AEM'
time_step = 200
dataset = sequence.getAll(ticker)
outputset = sequence.getAllPrices(ticker)
scaler = MinMaxScaler(feature_range=(0, 1))
priceScaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(dataset)
inputset = sequence.get3dData(scaled, time_step)
outputset = priceScaler.fit_transform(outputset)
dataset_size = len(scaled)
train_percent = 0.7

train_size = math.floor(train_percent * dataset_size)
test_size = dataset_size - train_size
predict_length=1
# Generators
#train_generator = MongoSequence(train_size, 2, query={'ticker':'AEM'})
#test_generator = MongoSequence(test_size, 2, query={'ticker':'AEM'})

#data
#train_dataset = sequence.get('AEM',train_size,pymongo.ASCENDING)
#test_dataset = sequence.get('AEM',test_size,pymongo.DESCENDING)

start = 500
train_X = inputset[start:train_size]
test_X = inputset[train_size:]
train_y = outputset[start+time_step:train_size+time_step]
test_y = outputset[train_size+time_step:]

print(train_X.shape)
print(test_X.shape)
print(train_y.shape)
print(test_y.shape)

# This returns a tensor
inputs = Input(shape=(8,))

model = Sequential()
model.add(LSTM(200, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mae')

if os.path.exists('aem_lstm_weights.h5'):
    model.load_weights('aem_lstm_weights.h5')
history = model.fit(train_X, train_y, epochs=10, batch_size=30, validation_data=(test_X, test_y), verbose=2, shuffle=False)

#save weights
model.save_weights('aem_lstm_weights.h5')

#predict_here, change time_step to current (-1)
input = np.array([inputset[-time_step,:]])
prediction = model.predict(input)
prediction = priceScaler.inverse_transform(prediction)
print(prediction)

# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()
