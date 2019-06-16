import importlib.util
lstm_spec = importlib.util.spec_from_file_location("module.name", "../neuralNetworks/price_lstm.py")
lstm = importlib.util.module_from_spec(lstm_spec)
lstm_spec.loader.exec_module(lstm)

supportedStocks = open('./supportedList','r')
tickers = supportedStocks.read().split('\n')
tickers = tickers[0:-1]
for ticker in tickers:
    
