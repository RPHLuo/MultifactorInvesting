import numpy as np
import seq_fundamental_lstm, seq_technical_lstm, seq_fundamental_cnn, seq_technical_cnn
import target_fundamental_ffnn, target_technical_cnn, target_fundamental_lstm

def run(ticker='AEM', dateNumber=20190530, time_step=200, path='./'):
    seq_result_1=seq_fundamental_lstm.run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)
    seq_result_2=seq_technical_lstm.run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)
    seq_result_3=seq_fundamental_cnn.run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)
    seq_result_4=seq_technical_cnn.run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)
    target_result_1=target_fundamental_ffnn.run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)
    target_result_2=target_technical_cnn.run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)
    target_result_3=target_fundamental_lstm.run(ticker=ticker, dateNumber=dateNumber, time_step=time_step, path=path)

    seq_results = [seq_result_1, seq_result_2, seq_result_3, seq_result_3]
    seq_results = np.array(seq_results)
    target_results = [target_result_1, target_result_2, target_result_3]
    target_results = np.array(target_results)
    # sum across ensemble members
    print(seq_results.shape)
    seq_results = np.average(seq_results, axis=0).flatten()
    print(seq_results)

    print(target_results.shape)
    target_results = np.average(target_results, axis=0).flatten()
    print(target_results)
    return target_results, seq_results
