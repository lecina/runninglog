import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
#import matplotlib.pyplot as plt

from utilities import utilities


def find_coefficient(df, xcol, ycol):
    #import statsmodels.formula.api as sm
    #result = sm.ols(formula = 'avg_pace ~ date_delta', data = df).fit()
    #print result.summary()

    y = df[ycol].values.reshape(-1,1)
    x = df[xcol].values.reshape(-1,1)

    model = LinearRegression()
    model.fit(x,y) 

    return model


def compute_models(df_all, xcol, ycol, chosen_types):
    models = {} 
    for running_type in chosen_types:
        df = df_all.loc[(df_all.type == running_type) & (df_all.avg_pace < 260)] #tmp solution. will use climb when data is available
        model = find_coefficient(df, xcol, ycol)
        models[running_type] = model

    return(models)

def get_runType_colors():
    runType_colors = {  'M':'#ff7f0e', # safety orange
                        'T':'#2ca02c', # cooked asparagus green
                        'I':'#d62728', # brick red
                        'R':'#9467bd' # muted purple
                    }

    return runType_colors

def get_figure(df, models, running_type, runType_colors):
    model = models[running_type]
    df_chosen_type = df[df['type'] == running_type]
    color = runType_colors[running_type]
    
    x_reg = np.linspace(min(df_chosen_type['date_delta']),
                        max(df_chosen_type['date_delta']),
                        num = 100
                        ).reshape(-1,1)
    x_date = np.datetime64(min(df.date)) + x_reg.astype('timedelta64[D]')

    return {
        'data': [
            go.Scatter(
                x=df_chosen_type['date'],
                y=df_chosen_type['avg_pace'],
                text=running_type,
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 10,#df_chosen_type['climb'],
                    'line': {'width': 0.5, 'color': 'white'},
                    'color': color
                },
                name=running_type
            ) #for running_type in chosen_types
            ,
            go.Scatter(
                x=x_date.flatten(),
                y=model.predict(x_reg).flatten(),
                name='Regression',
                mode='lines',
                hovertext=model.coef_
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Pace (s/km)'},
            margin={'l': 50, 'b': 50, 't': 50, 'r': 50},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            title='%s intervals'%running_type
        )
    }

def get_figure_all(df, models, running_types, runType_colors):
    traces = [
        go.Scatter(
            x=df[df['type'] == running_type]['date'],
            y=df[df['type'] == running_type]['avg_pace'],
            text=running_type,
            mode='markers',
            opacity=0.7,
            marker={
                'size': 10,#df_chosen_type['climb'],
                'line': {'width': 0.5, 'color': 'white'},
                'color': runType_colors[running_type]
            },
            name=running_type
        ) for running_type in running_types
    ]

    x_reg = np.linspace(min(df['date_delta']),
                        max(df['date_delta']),
                        num = 100).reshape(-1,1)
    x_date = (np.datetime64(min(df.date)) + x_reg.astype('timedelta64[D]')).flatten()
    traces.extend([
        go.Scatter(
            x=x_date,
            y=models[running_type].predict(x_reg).flatten(),
            #name='Regression',
            #color='orange',
            mode='lines',
            hovertext=models[running_type].coef_
        ) for running_type in running_types
    ])

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Date'},
            yaxis={'title': 'Pace (s/km)'},
            margin={'l': 50, 'b': 50, 't': 50, 'r': 50},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            title='Pace in intervals'
        )
    }

def get_summary_str(models, running_type):
    model = models[running_type]
    return "Improving %s at %.2f sec/month and %.2f sec/year"%(running_type, model.coef_*30,365*model.coef_)


def main():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    df = utilities.read_pandas_pickle("../../running_log_data/processed/df_struct.pkl")

    df.loc[:,'date_delta'] = (df['date'] - df['date'].min())  / np.timedelta64(1,'D')
    chosen_types = ['M', 'T', 'I', 'R']

    models = compute_models(df, xcol='date_delta', ycol='avg_pace', chosen_types=chosen_types)

    runType_colors = get_runType_colors()

    app.layout = html.Div([
        html.Div([
            html.Div([html.H3("Pace in structured workouts"),]),
            html.Div([
                dcc.Graph(
                    id='all-evol',
                    figure=get_figure_all(df,models, chosen_types, runType_colors)
                )
            ]),
            html.Div([html.P(get_summary_str(models, 'T')),],style={'height':'30px', 'textAlign':'center'}),
            html.Div([html.P(get_summary_str(models, 'I')),],style={'height':'30px', 'textAlign':'center'}),
            html.Div([html.P(get_summary_str(models, 'M')),],style={'height':'30px', 'textAlign':'center'}),
            html.Div([html.P(get_summary_str(models, 'R')),],style={'height':'30px', 'textAlign':'center'}),
        ]),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='T-evol',
                    figure=get_figure(df,models,'T', runType_colors)
                ),
                html.Div([html.H6(get_summary_str(models,'T')),],style={'height':'30px', 'textAlign':'center'}),
            ])
        ], style={'width':'49%', 'display': 'inline-block'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='I-evol',
                    figure=get_figure(df,models,'I', runType_colors)
                ),
                html.Div([html.H6(get_summary_str(models,'I')),],style={'height':'30px', 'textAlign':'center'}),
            ])
        ], style={'width':'49%', 'display': 'inline-block'}),

        html.Div([], style={'height':'30px'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='M-evol',
                    figure=get_figure(df,models,'M', runType_colors)
                ),
                html.Div([html.H6(get_summary_str(models,'M')),],style={'height':'30px', 'textAlign':'center'}),
            ])
        ], style={'width':'49%', 'display': 'inline-block'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='R-evol',
                    figure=get_figure(df,models,'R', runType_colors)
                ),
                html.Div([html.H6(get_summary_str(models,'R')),],style={'height':'30px', 'textAlign':'center'}),
            ])
        ], style={'width':'49%', 'display': 'inline-block'}),
    ])

    return app


if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
