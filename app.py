from flask import Flask
import os
from dotenv import load_dotenv
import quandl
import yfinance
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import plotly.offline as py

load_dotenv()

quandl.ApiConfig.api_key = os.getenv('QUANDL_KEY')

def build_model(ticker):
    msft_obj = yfinance.Ticker(ticker)
    msft_df = msft_obj.history(period='max')
    msft = msft_df.reset_index()[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
    m = Prophet()
    m.fit(msft)
    return m

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route('/')
def hello_world():
    return 'YEEHAW'

@app.route('/<tickername>')
def predict(tickername):
    m = build_model(tickername)
    future = m.make_future_dataframe(periods=30)
    forecast = m.predict(future)
    return forecast.to_html()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)