import pandas as pd
import yfinance


def fetch_data(ticker: str, period: str = 'max') -> pd.DataFrame:
    """
    Get data from Yahoo finance
    :param ticker: Finance ticker symbol
    :param period: Parameter to pass a yfinance.Ticker object
    :return:
    """
    ticker_obj = yfinance.Ticker(ticker)
    return ticker_obj.history(period=period).reset_index()
