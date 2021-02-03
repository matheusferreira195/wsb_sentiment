import praw
from textblob import TextBlob
import dash
import datetime
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque

client_id = 'HRP_psCzwyMwXg'
client_secret = 'AVBYc6nLZz_R3qCcYXI_AdfZWH95Gg'
user_agent = 'sentiment_analysis_wsb by /u/sadboy69195'

reddit_api = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

wsb = reddit_api.subreddit('wallstreetbets')

def data_listener(X,Y):
    for comment in wsb.stream.comments():
        if comment.link_author == 'AutoModerator' and 'Daily' in comment.link_title:

            analysis = TextBlob(comment.body)

            y_vec = analysis.sentiment.polarity
            x_vec = datetime.datetime.now()

            Y.append(y_vec)
            X.append(x_vec)

            break

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000
        ),
    ]
)

X = deque(maxlen=20)
Y = deque(maxlen=20)

@app.callback(Output('live-graph', 'figure'),
              [Input('graph-update', 'n_intervals')])
def update_graph_scatter(input_data):

    data_listener(X, Y)

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080 ,debug=True)
