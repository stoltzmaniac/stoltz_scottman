from flask import Flask
import plotly.graph_objects as go
from utils import fetch_data

# Instantiate an app
app = Flask(__name__)


@app.route('/')
def home():
    return 'Use the following endpoint: /data/tickername OR /plot/tickername'


@app.route('/data/<tickername>')
def data(tickername):
    data = fetch_data(tickername)
    return data.to_html()


@app.route('/plot/<tickername>')
def plot(tickername):
    data = fetch_data(tickername)
    fig = go.Figure([go.Scatter(x=data['Date'], y=data['Close'])])
    return fig.to_html()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
