import os, sys
lib_path = os.path.abspath(os.path.join('../neuralNetworks'))
sys.path.append(lib_path)
import price_lstm, target_ffnn

supportedStocks = open('./supportedList','r')
tickers = supportedStocks.read().split('\n')
tickers = tickers[0:-1]
for ticker in tickers:
    target_ffnn.train(ticker=ticker, performance_indicator=200, start=0, epochs=10)
    price_lstm.train(ticker=ticker, time_step=200, start=0, epochs=10)
    target_ffnn.run(ticker=ticker, dateNumber=20180608, time_step=200)
    price_lstm.run(ticker=ticker, dateNumber=20180608, time_step=200)
