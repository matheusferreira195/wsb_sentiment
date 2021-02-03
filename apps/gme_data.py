import yfinance

def gme_stock_price():
    data = yfinance.download(tickers='GME', period='1d', interval='1m')

    return data