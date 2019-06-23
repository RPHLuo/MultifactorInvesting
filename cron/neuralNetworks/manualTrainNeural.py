import os, sys
path = './'
lib_path = os.path.abspath(os.path.join(path))
sys.path.append(lib_path)
import price_lstm, target_ffnn, technical_cnn

supportedStocks = open('./supportedList','r')
tickers = supportedStocks.read().split('\n')
tickers = tickers[0:-1]
for ticker in tickers:
    target_ffnn.train(ticker=ticker, performance_indicator=200, start=0, epochs=10, path=path)
    price_lstm.train(ticker=ticker, time_step=200, start=0, epochs=10, path=path)
    technical_cnn.train(ticker=ticker, time_step=200, start=0, epochs=10, path=path)
