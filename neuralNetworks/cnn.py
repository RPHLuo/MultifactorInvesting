from keras.layers import Input, Dropout, Dense
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
performance_indicator = 200
dataset = sequence.getAll(ticker)
outputset = sequence.getAllPrices(ticker)
scaler = MinMaxScaler(feature_range=(0, 1))
priceScaler = MinMaxScaler(feature_range=(0, 1))
inputset = scaler.fit_transform(dataset)
outputset = priceScaler.fit_transform(outputset)
dataset_size = len(inputset)
train_percent = 0.7

train_size = math.floor(train_percent * dataset_size)
test_size = dataset_size - train_size
# Generators
#train_generator = MongoSequence(train_size, 2, query={'ticker':'AEM'})
#test_generator = MongoSequence(test_size, 2, query={'ticker':'AEM'})

#data
#train_dataset = sequence.get('AEM',train_size,pymongo.ASCENDING)
#test_dataset = sequence.get('AEM',test_size,pymongo.DESCENDING)

start = 0
train_X = inputset[start:train_size]
test_X = inputset[train_size:-performance_indicator]
train_y = outputset[start+performance_indicator:train_size+performance_indicator]
test_y = outputset[train_size+performance_indicator:]

print(train_X.shape)
print(test_X.shape)
print(train_y.shape)
print(test_y.shape)

model = Sequential()
model.add(Dense(32, activation='relu', input_shape=(train_X.shape[1],)))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='sgd',
              loss='binary_crossentropy',
              metrics=['accuracy'])

#uncomment to load model
#if os.path.exists('aem_cnn_weights.h5'):
#    model.load_weights('aem_cnn_weights.h5')
history = model.fit(train_X, train_y, epochs=100, batch_size=32, validation_data=(test_X, test_y), verbose=2, shuffle=False)

#save weights
model.save_weights('aem_cnn_weights.h5')

#predict_here, change performance_indicator to current (-1)
input = np.array([inputset[-performance_indicator,:]])
prediction = model.predict(input)
prediction = priceScaler.inverse_transform(prediction)
print(prediction)
# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
pyplot.show()
