import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import umap
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

from utilities import utilities
from constants import blockNames
from viz.viz_constants import viz_constants

def main():
    #external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    #app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app = dash.Dash(__name__)

    df = utilities.read_pandas_pickle("data/processed/df.pkl")

    runTypesToColors = viz_constants.get_runType_colors()

    cols = ['climb', u'distance', 'time']#, 'trail']

    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df[cols])
    reducer = umap.UMAP(n_neighbors=5, min_dist=0.25)
    embedding = reducer.fit_transform(df_scaled)
    import pickle
    #pickle.dump(embedding, open( "embedding.pkl", "wb" ) )
    embedding = pickle.load( open( "embedding.pkl", "rb" ) )

    df = pd.concat([df, pd.DataFrame(embedding, columns=['X1', 'X2'])], axis=1, sort=False)

    cols.extend(['date', 'type', 'where', u'distE', u'distI', u'distM', u'distR', u'distT', u'distX', u'distXB', 'trail'])

    app.layout = html.Div([
        dcc.Graph(figure= {
            'data': [go.Scatter(
                x=df.loc[:, 'X1'],
                y=df.loc[:, 'X2'],
                text=[df.loc[i,cols].to_string().replace("\n", "<br>") for i in range(len(df.index))],
                mode='markers',
                showlegend = True,
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {'width': 1, 'color': ['white' if x==0 else 'black' for x in df.trail]},
                    'symbol' : ['circle' if x==0 else 'diamond' for x in df.trail],
                    'color' : [runTypesToColors[x] for x in df.type]
                }
            )],
            'layout': go.Layout(
                xaxis={
                    'title': 'X1',
                    'type': 'linear'
                },
                yaxis={
                    'title': 'X2',
                    'type': 'linear'
                },
                showlegend = True,
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )
        }
        )
    ])

    return app


if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
