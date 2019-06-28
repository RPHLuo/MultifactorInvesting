import os, sys
path = './neuralNetworks/'
lib_path = os.path.abspath(os.path.join(path))
sys.path.append(lib_path)
import seq_fundamental_lstm, target_fundamental_ffnn, target_technical_cnn

supportedStocks = open('./supportedList','r')
tickers = supportedStocks.read().split('\n')
tickers = tickers[0:-1]
for ticker in tickers:
    target_fundamental_ffnn.run(ticker=ticker, dateNumber=20180608, time_step=200, path=path)
    seq_fundamental_lstm.run(ticker=ticker, dateNumber=20180608, time_step=200, path=path)
    target_technical_cnn.run(ticker=ticker, dateNumber=20180608, time_step=200, path=path)
