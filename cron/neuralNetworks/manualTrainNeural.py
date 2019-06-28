import os, sys
path = './'
lib_path = os.path.abspath(os.path.join(path))
sys.path.append(lib_path)
import seq_fundamental_lstm, seq_technical_lstm, seq_fundamental_cnn, seq_technical_cnn
import target_fundamental_ffnn, target_technical_cnn, target_fundamental_lstm

supportedStocks = open('../supportedList','r')
tickers = supportedStocks.read().split('\n')
tickers = tickers[0:-1]
for ticker in tickers:
    seq_fundamental_lstm.train(ticker=ticker, time_step=200, start=0, epochs=2, path=path)
    seq_technical_lstm.train(ticker=ticker, time_step=200, start=0, epochs=2, path=path)
    seq_fundamental_cnn.train(ticker=ticker, time_step=200, start=0, epochs=2, path=path)
    seq_technical_cnn.train(ticker=ticker, time_step=200, start=0, epochs=2, path=path)
    target_fundamental_ffnn.train(ticker=ticker, time_step=200, start=0, epochs=10, path=path)
    target_technical_cnn.train(ticker=ticker, time_step=200, start=0, epochs=10, path=path)
    target_fundamental_lstm.train(ticker=ticker, time_step=200, start=0, epochs=10, path=path)
