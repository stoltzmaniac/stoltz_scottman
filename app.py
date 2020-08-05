import os
import pickle
from flask import Flask
import plotly.graph_objects as go
from utils import fetch_data, fit_arima_model, append_forecast

# Instantiate an app
app = Flask(__name__)

# Read in all models
all_models_in_dir = os.listdir('models')
MODELS = {}
for i in all_models_in_dir:
    with open(f'models/{i}', 'rb') as f:
        tmp = pickle.load(f)
    MODELS[i[:-4]] = tmp





@app.route('/')
def home():
    return 'Use the following endpoint: /data/tickername OR /plot/tickername'


@app.route('/data/<tickername>')
def data(tickername):
    data = fetch_data(tickername)
    return data.reset_index().to_html()


@app.route('/build_model/<tickername>')
def build_model(tickername):
    data = fetch_data(tickername)
    model = fit_arima_model(data)
    MODELS[tickername] = model
    with open(f"models/{tickername}.pkl", 'wb') as f:
        pickle.dump(model, f)
    return "BUILT MODEL"


@app.route('/forecast/<tickername>/<steps>')
def forecast(tickername, steps):
    model = MODELS[tickername]
    return append_forecast(model, steps)


@app.route('/plot/<tickername>')
def plot(tickername):
    data = fetch_data(tickername).reset_index()
    fig = go.Figure([go.Scatter(x=data['Date'], y=data['Close'])])
    return fig.to_html()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
