import yfinance as yf

def get_stock_data(ticker):

    stock = yf.Ticker(ticker)

    data = stock.history(period="1d", interval="5m")

    return data