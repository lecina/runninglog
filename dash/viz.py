import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import numpy as np

df = pd.read_pickle("../../running_log_data/processed/df.pkl")
df.date = pd.to_datetime(df.date)

years = df.date.dt.year
year_marks={str(year): str(year) for year in np.hstack([years.unique(), [years.max()+1]])}
year_marks[str(years.max()+1)] = 'All'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_cols = list(df.columns)
available_cols.append('week')

app.layout = html.Div([
    html.Div([
        html.Div([
            #html.Div([dcc.Markdown('''Choose date:''')], style={'padding':'0px 0px 0px 10px'}),
            html.Div([
                dcc.Slider(
                    id='year--slider',
                    min=df.date.dt.year.min(),
                    max=df.date.dt.year.max()+1,
                    value=df.date.dt.year.max()+1,
                    step=1,
                    marks=year_marks,
                    included=False
                )], style={'width': '49%', 'display': 'inline-block', 'padding': '0px 0px 0px 20px'}),
            html.Div([
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=df.date.min(),
                    end_date=df.date.max(),
                    first_day_of_week=1,
                    display_format = "D/M/YYYY")
            ], style={  
                        'width': '35%', 
                        'float': 'right', 
                        'display': 'inline-block', 
                        'align-items': 'center',
                        'padding': '0px 0px 0px 0px'
                    })
            ]),
        html.Div([
            #dcc.Markdown('''Choose type:'''),
            dcc.Dropdown(
                id='type-dropdown',
                options=[
                    {'label': 'Easy pace', 'value': 'E'}, #todo: read it from runTypes
                    {'label': u'Threshold', 'value': 'T'},
                    {'label': 'Interval', 'value': 'I'},
                    {'label': 'Repetitions', 'value': 'R'},
                    {'label': 'Race', 'value': 'C'},
                    {'label': 'Cross training', 'value': 'X'}
                ],
                value=['E', 'T', 'I', 'R', 'C'],
                multi = True
            )], style={'padding':'20px 10px 10px 10px'})
    ]),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_cols],
                value='distance'
            ),
            dcc.Checklist(
                id='yaxis-type',
                options=[ {'label': 'Log', 'value': 'Log'},],
                values=[],
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block', 'padding':'0px 0px 0px 10px'}),

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_cols],
                value='time'
            ),
            dcc.Checklist(
                id='xaxis-type',
                options=[ {'label': 'Log', 'value': 'Log'},],
                values=[],
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    dcc.Graph(id='graph1')
    ], style = {'width' : '49%', 'display':'inline-block'}),
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_cols],
                value='distance'
            ),
            dcc.Checklist(
                id='yaxis-type2',
                options=[ {'label': 'Log', 'value': 'Log'},],
                values=[],
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block', 'padding':'0px 0px 0px 10px'}),
        html.Div([
            dcc.Dropdown(
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_cols],
                value='date'
            ),
            dcc.Checklist(
                id='xaxis-type2',
                options=[ {'label': 'Log', 'value': 'Log'},],
                values=[],
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    dcc.Graph(id='graph2')
    ], style = {'width' : '49%', 'display': 'inline-block'})
])


@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'values'),
     dash.dependencies.Input('yaxis-type', 'values'),
     dash.dependencies.Input('type-dropdown', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_figure(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 selected_types, chosen_year,
                 start_date, end_date):

    if chosen_year == df.date.dt.year.max()+1:
        filt_df = df
    else:
        filt_df = df[df.date.dt.year == chosen_year]

    filt_df = filt_df[np.logical_and(filt_df.date >= start_date, filt_df.date <= end_date)]

    xaxis_dict = {'title':xaxis_column_name}
    if xaxis_type == ['Log']: xaxis_dict['type'] = 'log'
    yaxis_dict = {'title':yaxis_column_name}
    if yaxis_type == ['Log']: yaxis_dict['type'] = 'log'


    traces = [
                go.Scatter(
                    x=filt_df[filt_df['type'] == i][xaxis_column_name],
                    y=filt_df[filt_df['type'] == i][yaxis_column_name],
                    text=filt_df[filt_df['type'] == i]['date'],
                    mode='markers',
                    opacity=0.5,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in selected_types 
    ]

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis=xaxis_dict,
            yaxis=yaxis_dict,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value'),
     dash.dependencies.Input('xaxis-type2', 'values'),
     dash.dependencies.Input('yaxis-type2', 'values'),
     #dash.dependencies.Input('type-dropdown', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_figure(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 chosen_year,
                 start_date, end_date):

    if chosen_year == df.date.dt.year.max()+1:
        filt_df = df
    else:
        filt_df = df[df.date.dt.year == chosen_year]

    filt_df = filt_df[np.logical_and(filt_df.date >= start_date, filt_df.date <= end_date)]

    xaxis_dict = {'title':xaxis_column_name}
    if xaxis_type == ['Log']: xaxis_dict['type'] = 'log'
    yaxis_dict = {'title':yaxis_column_name}
    if yaxis_type == ['Log']: yaxis_dict['type'] = 'log'

    #TODO:move code
    if xaxis_column_name == 'week' or yaxis_column_name == 'week':
        filt_df['week'] = filt_df.date.apply(lambda x: x.isocalendar()[1])
        filt_df = filt_df[:][['distance', 'distE', 'distM', 'distT', 'distI', 'distR']].groupby(filt_df['week']).sum()
        filt_df['week'] = filt_df.index
        print filt_df


    if yaxis_column_name == 'distance':
        types = ['E', 'M', 'T', 'I', 'R']
        distance_template = 'dist%s'
        traces = [
                    go.Bar(
                        x=filt_df[:][xaxis_column_name],
                        y=filt_df[:][distance_template%i],
                        #text=filt_df[:]['date'],
                        #mode='markers',
                        opacity=0.5,
                        #marker={ 'size': 15, 'line': {'width': 0.5, 'color': 'white'} },
                        name=i
                    ) for i in types 
        ]
    else:
        traces = [
                    go.Bar(
                        x=filt_df[:][xaxis_column_name],
                        y=filt_df[:][yaxis_column_name],
                        #text=filt_df[:]['date'],
                        #mode='markers',
                        opacity=0.5,
                        #marker={ 'size': 15, 'line': {'width': 0.5, 'color': 'white'} },
                        name='All'
                    ) 
        ]

    return {
        'data': traces,
        'layout': go.Layout(
            barmode='stack',
            xaxis=xaxis_dict,
            yaxis=yaxis_dict,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
