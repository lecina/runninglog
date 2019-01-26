import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import dash_table

import pandas as pd
import numpy as np

from constants import blockNames

df = pd.read_pickle("../../running_log_data/processed/df.pkl")
df.date = pd.to_datetime(df.date)

years = df.date.dt.year
year_marks={str(year): str(year) for year in np.hstack([years.unique(), [years.max()+1]])}
year_marks[str(years.max()+1)] = 'All'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

runType_order = [blockNames.RunTypes.E, 
                 blockNames.RunTypes.M,
                 blockNames.RunTypes.T,
                 blockNames.RunTypes.I,
                 blockNames.RunTypes.R,
                 blockNames.RunTypes.C,
                 blockNames.RunTypes.X]
colors = [  '#1f77b4', # muted blue
            '#ff7f0e', # safety orange
            '#2ca02c', # cooked asparagus green
            '#d62728', # brick red
            '#9467bd', # muted purple
            '#17becf', # blue-teal
            #'#e377c2', # raspberry yogurt pink
            #'#7f7f7f', # middle gray
            #'#bcbd22', # curry yellow-green
            '#8c564b'] # chestnut brown
runTypesToColors = {runType_order[i]:colors[i] for i in range(len(runType_order))}

available_run_types = [{'value':rt, 'label':blockNames.RUN_TYPES_LONG_NAME_DICTIONARY[rt] } for rt in runType_order]

basicRunning_types = [blockNames.RunTypes.E, 
                     blockNames.RunTypes.M,
                     blockNames.RunTypes.T,
                     blockNames.RunTypes.I,
                     blockNames.RunTypes.R,
                     blockNames.RunTypes.X]

available_cols = list(df.columns)
available_cols.append('week')

time_agg_options = ['day', 'week', 'month', 'year']


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app.layout = html.Div([
    html.Div([
        html.Div([
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
            dcc.Dropdown(
                id='type-dropdown',
                options=available_run_types,
                value=[blockNames.RunTypes.X, blockNames.RunTypes.C, blockNames.RunTypes.R, blockNames.RunTypes.I, blockNames.RunTypes.T, blockNames.RunTypes.E],
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
                #options=[{'label': i, 'value': i} for i in ['distance']],
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
                options=[{'label': i, 'value': i} for i in time_agg_options],
                value='week'
            )
        ],style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
    dcc.Graph(id='graph2')
    ], style = {'width' : '49%', 'display': 'inline-block'}),
    html.Div([
        dash_table.DataTable(
                    data=df.to_dict('rows'),
                    #columns=[{'id': c, 'name': c} for c in df.columns],
                    columns=[
                            {"name": ["", "Date"], "id": "date"},
                            {"name": ["", "Type"], "id": "type"},
                            {"name": ["", "Dist."], "id": "distance"},
                            {"name": ["", "Climb"], "id": "climb"},
                            {"name": ["", "Time"], "id": "time"},
                            {"name": ["", "Where"], "id": "where"},
                            {"name": ["", "Notes"], "id": "notes"},
                            {"name": ["", "Avg. Pace"], "id": "avg_pace"},
                            {"name": ["Distances", "Dist. E"], "id": "distE"},
                            {"name": ["Distances", "Dist. M"], "id": "distM"},
                            {"name": ["Distances", "Dist. T"], "id": "distT"},
                            {"name": ["Distances", "Dist. I"], "id": "distI"},
                            {"name": ["Distances", "Dist. R"], "id": "distR"},
                            {"name": ["Distances", "Dist. X"], "id": "distX"},
                            {"name": ["Paces", "Pace E"], "id": "paceE"},
                            {"name": ["Paces", "Pace M"], "id": "paceM"},
                            {"name": ["Paces", "Pace T"], "id": "paceT"},
                            {"name": ["Paces", "Pace I"], "id": "paceI"},
                            {"name": ["Paces", "Pace R"], "id": "paceR"},
                            {"name": ["Paces", "Pace X"], "id": "paceX"},
                        ],
                    style_table={
                        'overflowX': 'scroll', 
                        'maxHeight': '300',
                        'overflowY': 'scroll'},
                    css=[{
                            'selector': '.dash-cell div.dash-cell-value',
                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                        }],
                    style_cell={
                        'whiteSpace': 'no-wrap',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'minWidth': '70px', 'maxWidth': '100px'
                    },
                    #n_fixed_columns=1,
                    n_fixed_rows=2,
                    style_as_list_view=True,
                    merge_duplicate_headers=True,
                    style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold'
                        },
                    sorting=True,
                    sorting_type="multi",
                ),
    ]),
    html.Div([
        dcc.Graph(id='graph3')
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
                        'line': {'width': 0.5, 'color': 'white'},
                        'color': runTypesToColors[i]
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
     dash.dependencies.Input('yaxis-type2', 'values'),
     dash.dependencies.Input('type-dropdown', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_figure(xaxis_column_name, yaxis_column_name,
                 yaxis_type, dropdown_types, chosen_year,
                 start_date, end_date):

    if chosen_year == df.date.dt.year.max()+1:
        filt_df = df
    else:
        filt_df = df[df.date.dt.year == chosen_year]

    filt_df = filt_df[filt_df.type.isin(dropdown_types)]

    filt_df = filt_df[np.logical_and(filt_df.date >= start_date, filt_df.date <= end_date)]

    xaxis_dict = {'title':xaxis_column_name}
    yaxis_dict = {'title':yaxis_column_name}
    if yaxis_type == ['Log']: yaxis_dict['type'] = 'log'

    #TODO:move code outside callback
    #TODO:generalize beyond distance
    if xaxis_column_name == 'day':
        xaxis_column_name = 'date'

    if yaxis_column_name == 'distance':
        distance_template = 'dist%s'
        basicDistances = [distance_template%bt for bt in basicRunning_types]
        basicDistances.extend(['distance', 'date'])
        if xaxis_column_name == 'week' or yaxis_column_name == 'week':
            filt_df = filt_df[:][basicDistances].resample('W', on='date').sum()
            filt_df['week'] = filt_df.index
        elif xaxis_column_name == 'month' or yaxis_column_name == 'month':
            filt_df = filt_df[:][basicDistances].resample('MS', on='date').sum()
            filt_df['month'] = filt_df.index
        elif xaxis_column_name == 'year' or yaxis_column_name == 'year':
            filt_df = filt_df[:][basicDistances].resample('YS', on='date').sum()
            filt_df['year'] = filt_df.index
    else:
        if xaxis_column_name == 'week' or yaxis_column_name == 'week':
            filt_df = filt_df[:][[yaxis_column_name, 'date']].resample('W', on='date').sum()
            filt_df['week'] = filt_df.index
        elif xaxis_column_name == 'month' or yaxis_column_name == 'month':
            filt_df = filt_df[:][[yaxis_column_name, 'date']].resample('MS', on='date').sum()
            filt_df['month'] = filt_df.index
        elif xaxis_column_name == 'year' or yaxis_column_name == 'year':
            filt_df = filt_df[:][[yaxis_column_name, 'date']].resample('YS', on='date').sum()
            filt_df['year'] = filt_df.index

    selected_basicRunning_types = [t for t in basicRunning_types if t in dropdown_types]


    if yaxis_column_name == 'distance':
        distance_template = 'dist%s'
        traces = [
                    go.Bar(
                        x=filt_df[:][xaxis_column_name],
                        y=filt_df[:][distance_template%i],
                        #text=filt_df[:]['date'],
                        #mode='markers',
                        opacity=0.5,
                        #marker={ 'size': 15, 'line': {'width': 0.5, 'color': 'white'} },
                        marker={ 'color': runTypesToColors[i] },
                        name=i
                    ) for i in selected_basicRunning_types
        ]
    else:
        traces = [
                    go.Bar(
                        x=filt_df[:][xaxis_column_name],
                        y=filt_df[:][yaxis_column_name],
                        #text=filt_df[:]['date'],
                        #mode='markers',
                        opacity=0.5,
                        #marker={ 'color': runTypesToColors[0] },
                        marker={ 'color': '#1f77b4' },
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
            bargap=0.05,
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('graph3', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('type-dropdown', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('date-picker-range', 'start_date'),
     dash.dependencies.Input('date-picker-range', 'end_date')])
def update_figure(xaxis_column_name, yaxis_column_name,
                 selected_types, chosen_year,
                 start_date, end_date):

    if chosen_year == df.date.dt.year.max()+1:
        filt_df = df
    else:
        filt_df = df[df.date.dt.year == chosen_year]

    filt_df = filt_df[np.logical_and(filt_df.date >= start_date, filt_df.date <= end_date)]

    data = [
        go.Histogram2dContour(
            x=filt_df[filt_df['type'].isin(selected_types)][xaxis_column_name],
            y=filt_df[filt_df['type'].isin(selected_types)][yaxis_column_name],
            colorscale = 'Blues',
            reversescale = True,
            xaxis = 'x',
            yaxis = 'y',
            nbinsx=25,
            nbinsy=25,
            ncontours=20,
            contours = dict(coloring="fill"),
            name='Density',
            histnorm="density"
        ),
        go.Histogram(
            y=filt_df[filt_df['type'].isin(selected_types)][yaxis_column_name],
            xaxis = 'x2',
            marker = dict( color = 'rgba(0,0,0,1)'),
            name="Histogram: %s"%yaxis_column_name
        ),
        go.Histogram(
            x=filt_df[filt_df['type'].isin(selected_types)][xaxis_column_name],
            yaxis = 'y2',
            marker = dict( color = 'rgba(0,0,0,1)'),
            name="Histogram: %s"%xaxis_column_name
        )
    ]

    scatter_traces = [
                go.Scatter(
                    x=filt_df[filt_df['type'] == i][xaxis_column_name],
                    y=filt_df[filt_df['type'] == i][yaxis_column_name],
                    text=filt_df[filt_df['type'] == i]['date'],
                    mode='markers',
                    opacity=0.5,
                    marker={
                        'size': 5,
                        'line': {'width': 0.5, 'color': 'white'},
                        'color': runTypesToColors[i]
                    },
                    xaxis = 'x',
                    yaxis = 'y',
                    name=i
                ) for i in selected_types 
    ]
    data.extend(scatter_traces)

    layout = go.Layout(
        autosize = True,
        xaxis = dict( zeroline = False, domain = [0,0.85], showgrid = False, title = xaxis_column_name),
        yaxis = dict( zeroline = False, domain = [0,0.85], showgrid = False, title = yaxis_column_name),
        xaxis2 = dict( zeroline = False, domain = [0.85,1], showgrid = False),
        yaxis2 = dict( zeroline = False, domain = [0.85,1], showgrid = False),
        height = 600,
        width = 600,
        bargap = 0,
        hovermode = 'closest',
        showlegend = False
    )

    fig = go.Figure(data=data,layout=layout)

    ##########
    x=filt_df[filt_df['type'] == i][xaxis_column_name]
    y=filt_df[filt_df['type'] == i][yaxis_column_name]
    fig = ff.create_2d_density(
        x, y,
        hist_color='rgb(255, 237, 222)', point_size=3
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
