import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

ticker_symbol = '^GSPC'

start_date = '2020-01-01'
end_date = '2024-01-01'

sp500_data = yf.download(ticker_symbol, start=start_date, end=end_date)

sp500_data = sp500_data[['Open', 'High', 'Low', 'Close']]

#print(sp500_data.head())