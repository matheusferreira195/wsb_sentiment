import yfinance
import datetime
import pytz
def gme_stock_price(X, Y):
    data = yfinance.download(tickers='GME', period='1d', interval='1m').reset_index()
    data = data.loc[data['Datetime'] > (datetime.datetime.now(pytz.timezone('US/Eastern')) - datetime.timedelta(minutes=1))]
    X.append(data['Datetime'])
    Y.append(data['Close'])
    return data