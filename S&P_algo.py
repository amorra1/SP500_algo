import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Download S&P 500 data
ticker_symbol = '^GSPC'
start_date = '2020-01-01'
end_date = '2024-01-01'
sp500_data = yf.download(ticker_symbol, start=start_date, end=end_date)
sp500_data = sp500_data[['Open', 'High', 'Low', 'Close']]

# Moving average function 
def calculateSMA(data, window=50):
    return data.rolling(window=window).mean()

# Trend check: 0 for downtrend, 1 for uptrend
def detectTrend(data, shortWindow=50, longWindow=200):
    signals = pd.DataFrame(index=data.index)
    signals['trend'] = 0.0
    
    shortMovAVG = calculateSMA(data['Close'], shortWindow).reindex(signals.index)
    longMovAVG = calculateSMA(data['Close'], longWindow).reindex(signals.index)
    
    signals['trend'][shortWindow:] = shortMovAVG.iloc[shortWindow:] > longMovAVG.iloc[longWindow:]
    
    return signals['trend']

# Generate trendlines
def generateTrendline(data, trend):
    trendlinePoints = []
    
    # Uptrend: Identify lowest candle points
    uptrendPoints = data.loc[trend].groupby((data.loc[trend].Close < data.loc[trend].Close.shift(1)).cumsum()).agg({'Low': 'min', 'High': 'max'})
    uptrendPoints = uptrendPoints.dropna()
    
    # Downtrend: Identify highest candle points
    downtrendPoints = data.loc[~trend].groupby((data.loc[~trend].Close > data.loc[~trend].Close.shift(1)).cumsum()).agg({'High': 'max', 'Low': 'min'})
    downtrendPoints = downtrendPoints.dropna()
    
    if not uptrendPoints.empty:
        trendlinePoints.extend(uptrendPoints[['Low', 'High']].values)
    if not downtrendPoints.empty:
        trendlinePoints.extend(downtrendPoints[['Low', 'High']].values)
        
    return np.array(trendlinePoints)


# Example usage
short_window = 50
long_window = 200
trend = detectTrend(sp500_data, short_window, long_window)
trendlines = generateTrendline(sp500_data, trend)

# Plotting the progress
plt.figure(figsize=(12, 6))
plt.plot(sp500_data.index, sp500_data['Close'], label='Close Price')
plt.plot(trendlines[:, 0], color='green', linestyle='--', label='Trendlines')
plt.plot(trendlines[:, 1], color='green', linestyle='--')
plt.title('S&P 500 with Trendlines')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()
