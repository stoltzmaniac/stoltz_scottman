import pickle
import matplotlib.pyplot as plt
import plotly.express as px
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import numpy as np
import yfinance


def fetch_data(ticker: str, period: str = 'max') -> pd.DataFrame:
    """
    Get data from Yahoo finance
    :param ticker: Finance ticker symbol
    :param period: Parameter to pass a yfinance.Ticker object
    :return:
    """
    ticker_obj = yfinance.Ticker(ticker)
    ticker_df = ticker_obj.history(period=period)
    ticker_df.index = pd.to_datetime(ticker_df.index)
    return ticker_df


def calc_time_series_metrics(time_series, metric='Close', start_year='2008', end_year='2020', mean_window=365, std_window=365, transform=None):
    time_series = time_series.copy()

    if transform == 'log':
        time_series[metric] = np.log(time_series[metric])

    time_series = time_series[start_year:end_year]
    time_series['rolling_mean'] = time_series[metric].rolling(mean_window).mean()
    time_series['rolling_std'] = time_series[metric].rolling(std_window).std()

    # Dickey Fuller
    adf = adfuller(time_series[metric], autolag='AIC')
    adf_output = pd.Series(adf[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])

    return {'time_series': time_series, 'adf': adf_output, 'transform': transform}


def calc_decomposed_time_series(time_series, metric='Close', start_year='2008', end_year='2020', model='additive', period=30, transform=None):
    time_series = time_series.copy()

    if transform == 'log':
        time_series[metric] = np.log(time_series[metric])

    time_series = time_series[start_year:end_year]
    return seasonal_decompose(time_series[metric], model=model, period=period)


def fit_arima_model(time_series, metric='Close', order_1=2, order_2=1, order_3=2):
    model = ARIMA(time_series[metric], order=(order_1, order_2, order_3))
    results = model.fit()
    return results


def append_forecast(fitted_model, steps):
    fcast = fitted_model.forecast(steps)
    return fcast


def plot_augmented_data(time_series, metric='Close'):
    time_series = time_series.copy().reset_index()
    fig = px.line(time_series, x='Date', y=metric)
    fig.add_scatter(x=time_series['Date'], y=time_series['rolling_mean'], mode='lines')
    fig.add_scatter(x=time_series['Date'], y=time_series['rolling_std'], mode='lines')
    # fig.show or fig.to_html()
    return fig






def test_stationarity_example(timeseries):
    # https://medium.com/@stallonejacob/time-series-forecast-a-basic-introduction-using-python-414fcb963000
    # Determing rolling statistics
    rolmean = timeseries.rolling(365).mean()
    rolstd = timeseries.rolling(365).std()
    # Plot rolling statistics:
    plt.plot(timeseries, color='blue', label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()
    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)

