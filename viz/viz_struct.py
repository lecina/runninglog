import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import datetime
import base64

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

from runninglog.utilities import utilities
try:
    from viz.viz_constants import viz_constants
except:
    from viz_constants import viz_constants

#TODO:move to common functions
def subtract_weeks(d, weeks=52):
    return d - datetime.timedelta(days=d.weekday() + 7*weeks)

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
        df = df_all.loc[(df_all.type == running_type)] #tmp solution. will use climb when data is available
        try:
            model = find_coefficient(df, xcol, ycol)
        except ValueError:
            class EmptyModel:
                def __init__(self):
                    self.coef_=0
                def predict(self, x): 
                    if len(x) > 1:
                        return np.array([0]*len(x))
                    return 0
            model = EmptyModel()
        models[running_type] = model

    return(models)

def get_figure(df, models, running_type, runType_colors):
    model = models[running_type]
    df_chosen_type = df[df['type'] == running_type]
    color = runType_colors[running_type]
    
    x_reg = np.linspace(min(df_chosen_type['date_delta']),
                        max(df_chosen_type['date_delta']),
                        num = 100
                        ).reshape(-1,1)
    x_date = np.datetime64(min(df.date)) + x_reg.astype('timedelta64[D]')

    opacities = df_chosen_type.trail.apply(lambda x : 0.35 if 1 else 0.7)

    return {
        'data': [
            go.Scatter(
                x=df_chosen_type.date[df_chosen_type.trail == False],
                y=df_chosen_type.avg_pace[df_chosen_type.trail == False],
                text=running_type,
                mode='markers',
                opacity= 0.7,
                marker={
                    'size': 10,#df_chosen_type['climb'],
                    'line': {'width': 0.5, 'color': 'white'},
                    'color': color
                },
                name=running_type
            ) #for running_type in chosen_types
            ,
            go.Scatter(
                x=df_chosen_type.date[df_chosen_type.trail == True],
                y=df_chosen_type.avg_pace[df_chosen_type.trail == True],
                text=running_type,
                mode='markers',
                opacity= 0.35,
                marker={
                    'size': 10,#df_chosen_type['climb'],
                    'line': {'width': 0.5, 'color': 'white'},
                    'color': color
                },
                name="%s (trail)"%running_type
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
            name='Reg.%s'%running_type,
            marker={
                'color': runType_colors[running_type]
            },
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
            hovermode='closest'
        )
    }

def get_summary_str(models, running_type):
    model = models[running_type]
    return "Improving **%s** at **%.2f sec/month** and **%.1f sec/year**"%(running_type, model.coef_*30,365*model.coef_)


def main():
    app = dash.Dash(__name__)

    df = utilities.read_pandas_pickle("data/processed/df_struct.pkl")

    year_marks = viz_constants.get_year_marks(df)

    df.loc[:,'date_delta'] = (df['date'] - df['date'].min())  / np.timedelta64(1,'D')
    chosen_types = ['M', 'T', 'I', 'R']

    models = compute_models(df[df.trail == 0], xcol='date_delta', ycol='avg_pace', chosen_types=chosen_types)

    runType_colors = viz_constants.get_runType_colors()

    encoded_image = base64.b64encode(open('img/logo.png', 'rb').read()).decode('ascii')

    app.layout = html.Div([
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'height':'40px', 'display':'inline-block', 'margin':'5px 0px 0px 10px'}),
           html.H2("Running log - Structure analysis", style={'display':'inline-block', 'vertical-align': 'center', 'margin':'0px', 'padding':'3px 0px 5px 20px'}) 
        ], style={'background-color':'#E57E7E', 'height':'50px', 'vertical-align': 'center', 'padding':'0px', 'margin':'0px', 'margin-block-start':'0px', 'display':'flex'}),
        html.Div([
            html.Div([
                dcc.Slider(
                    id='year-slider',
                    min=min(year_marks.keys()),
                    max=max(year_marks.keys()),
                    value=max(year_marks.keys()),
                    step=1,
                    marks=year_marks,
                    included=False
                )
            ], style={'width': '30%', 'display': 'inline-block'}),
            html.Div([
                dcc.Checklist(
                    id='chosen_types',
                    options=[
                        {'label': 'Running', 'value': 'Running'},
                        {'label': 'Mountaineering', 'value': 'X', 'disabled':True},
                        {'label': 'Biking', 'value': 'XB', 'disabled':True},
                    ],
                    value=['Running'],
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'display':'inline-block', 'vertical-align': 'top'}),
            html.Div([
                dcc.RadioItems(
                    id='trail_road_selector',
                    options=[
                        {'label': 'All', 'value': 'All'},
                        {'label': 'Road', 'value': 'Road'},
                        {'label': 'Trail', 'value': 'Trail'},
                    ],
                    value='Road',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'display':'inline-block', 'vertical-align': 'top'})
        ], style={'width':'100%', 'display':'flex','justify-content':'space-around','padding-top':'5px'}),
        html.Hr(style={'margin':'0px 0px 10px 0px'}),
        html.Div([
            html.Div([html.H3("Pace in structured workouts"),]),
            html.Div([ dcc.Graph( id='all-evol') ]),
            html.Div([dcc.Markdown(id='T_results'),],style={'height':'30px', 'textAlign':'center'}),
            html.Div([dcc.Markdown(id='I_results'),],style={'height':'30px', 'textAlign':'center'}),
            html.Div([dcc.Markdown(id='R_results'),],style={'height':'30px', 'textAlign':'center'}),
            html.Div([dcc.Markdown(id='M_results'),],style={'height':'30px', 'textAlign':'center'}),
        ]),
        html.Div([html.H3("Pace in road workouts"),]),
        html.Div([
            html.Div([
                dcc.Graph(
                    id='T-evol',
                    figure=get_figure(df, models,'T', runType_colors)
                ),
                html.Div([dcc.Markdown(get_summary_str(models,'T')),],style={'height':'30px', 'textAlign':'center'}),
            ])
        ], style={'width':'49%', 'display': 'inline-block'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='I-evol',
                    figure=get_figure(df,models,'I', runType_colors)
                ),
                html.Div([dcc.Markdown(get_summary_str(models,'I')),],style={'height':'30px', 'textAlign':'center'}),
            ])
        ], style={'width':'49%', 'display': 'inline-block'}),

        html.Div([], style={'height':'30px'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='M-evol',
                    figure=get_figure(df,models,'M', runType_colors)
                ),
                html.Div([dcc.Markdown(get_summary_str(models,'M')),],style={'height':'30px', 'textAlign':'center'}),
            ])
        ], style={'width':'49%', 'display': 'inline-block'}),

        html.Div([
            html.Div([
                dcc.Graph(
                    id='R-evol',
                    figure=get_figure(df,models,'R', runType_colors)
                ),
                html.Div([dcc.Markdown(get_summary_str(models,'R')),],style={'height':'30px', 'textAlign':'center'}),
            ])
        ], style={'width':'49%', 'display': 'inline-block'}),
    ])

    @app.callback(
        [dash.dependencies.Output('all-evol', 'figure'),
        dash.dependencies.Output('T_results', 'children'),
        dash.dependencies.Output('I_results', 'children'),
        dash.dependencies.Output('R_results', 'children'),
        dash.dependencies.Output('M_results', 'children')],
        [dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value'),
        dash.dependencies.Input('year-slider', 'value')])
    def update_figure_all(chosen_activities, trail_road_selector, chosen_year):
        if chosen_year == df.date.dt.year.max()+2:
            filt_df = df
        elif chosen_year == df.date.dt.year.max()+1:
            today = datetime.datetime.now()
            last_year = subtract_weeks(today, weeks=52)
            filt_df = df[np.logical_and(df.date >= last_year, df.date <= today)]
        else:
            filt_df = df[df.date.dt.year == chosen_year]

        chosen_activity_types = viz_constants.get_activities_from_checklist(chosen_activities)
        filt_df = filt_df[filt_df.type.isin(chosen_activity_types)]

        trail_road = viz_constants.get_trail_road_activities(trail_road_selector)
        filt_df = filt_df[filt_df.trail.isin(trail_road)]

        running_types = ['M', 'T', 'I', 'R']
        filt_df.loc[:,'date_delta'] = (filt_df['date'] - filt_df['date'].min())  / np.timedelta64(1,'D')
        models = compute_models(filt_df, xcol='date_delta', ycol='avg_pace', chosen_types=running_types)
        return get_figure_all(filt_df, models, running_types, viz_constants.get_runType_colors()),\
                get_summary_str(models, 'T'),\
                get_summary_str(models, 'I'),\
                get_summary_str(models, 'R'),\
                get_summary_str(models, 'M')


    return app


if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
