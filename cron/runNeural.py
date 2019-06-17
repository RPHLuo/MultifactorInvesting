import os, sys
path = '../neuralNetworks/'
lib_path = os.path.abspath(os.path.join(path))
sys.path.append(lib_path)
import price_lstm, target_ffnn

supportedStocks = open('./supportedList','r')
tickers = supportedStocks.read().split('\n')
tickers = tickers[0:-1]
for ticker in tickers:
    target_ffnn.run(ticker=ticker, dateNumber=20180608, performance_indicator=200, path=path)
    price_lstm.run(ticker=ticker, dateNumber=20180608, time_step=200, path=path)
