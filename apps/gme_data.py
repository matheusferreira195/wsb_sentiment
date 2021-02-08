import yfinance
import datetime
import pytz
def gme_stock_price():
    data = yfinance.download(tickers='GME', period='1d', interval='1m').reset_index()
    return (data)