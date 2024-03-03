import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

ticker_symbol = '^GSPC'
start_date = '2020-01-01'
end_date = '2024-01-01'
sp500_data = yf.download(ticker_symbol, start=start_date, end=end_date)
sp500_data = sp500_data[['Open', 'High', 'Low', 'Close']]

#print(sp500_data.head())

#Moving average function 
def calculateSMA(data, window=50):
    return data.rolling(windiow=window).mean()

#trend check, 0 for downtrend, 1 for uptrend
def detectTrend(data, shortWindow=50, longWindow=200):
    signals = pd.DataFrame(index=data.index)
    signals['trend'] = 0.0
    
    signals['shortMovAVG'] = calculateSMA(data['Close'], shortWindow)
    
    signals['longMovAVG'] = calculateSMA(data['Close'], longWindow)
    
    signals['trend'][shortWindow:] = \
        signals['shortMovAVG'][shortWindow:] > signals['longMovAVG'][longWindow:]
    
    return signals['trend']

signals = detectTrend(sp500_data)
