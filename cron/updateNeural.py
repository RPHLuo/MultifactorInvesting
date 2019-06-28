import os, sys
path = './neuralNetworks/'
lib_path = os.path.abspath(os.path.join(path))
sys.path.append(lib_path)
import seq_fundamental_lstm, target_fundamental_ffnn, target_technical_cnn

supportedStocks = open('./supportedList','r')
tickers = supportedStocks.read().split('\n')
tickers = tickers[0:-1]
for ticker in tickers:
    target_fundamental_ffnn.train(ticker=ticker, time_step=200, start=0, epochs=10, path=path)
    seq_fundamental_lstm.train(ticker=ticker, time_step=200, start=0, epochs=10, path=path)
    target_technical_cnn.train(ticker=ticker, time_step=200, start=0, epochs=10, path=path)
