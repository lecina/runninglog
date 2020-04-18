import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.tools import FigureFactory as ff
#import seaborn as sns
import matplotlib.pyplot as plt
import dash_table
import datetime
import base64

import pandas as pd
import numpy as np

from constants import blockNames
from single_run import runTypes

try:
    from viz.viz_constants import viz_constants
except:
    from viz_constants import viz_constants
try:
    from viz.viz_exploration import update_distr_plot_figure
except:
    from viz_exploration import update_distr_plot_figure

def read_pandas_pickle(fname = "data/processed/df.pkl"):
    df = pd.read_pickle(fname)
    df.date = pd.to_datetime(df.date)
    return df


def get_ordered_runType_long_name(runType_order):
    return [{'value':rt, 'label':blockNames.RUN_TYPES_LONG_NAME_DICTIONARY[rt] } for rt in runType_order]

def get_available_columns():
    available_cols = ['distance', 'distance road vs trail', 'time', 'climb', 'avg_pace', '%types', 'feeling']
    return available_cols

def get_time_options():
    time_agg_options = ['week', 'month', 'year']
    return time_agg_options

def get_running_location_count(df,column):
    counts = pd.crosstab(index=df[column], columns="count") 
    rel_counts = counts/counts.sum()*100
    counts = pd.concat([counts, rel_counts], axis=1)
    counts.columns = ['counts','rel_counts']
    return counts

def subtract_weeks(d, weeks=52):
    return d - datetime.timedelta(days=d.weekday() + 7*weeks)

def record_table_columns():
    columns=[
            {"name": "Date", "id": "date"},
            {"name": "Time", "id": "time"},
            {"name": "Climb", "id": "climb"},
            {"name": "V.speed", "id": "vspeed"},
            {"name": "Pace", "id": "avg_pace"},
            {"name": "Route", "id": "route"},
            {"name": "Type", "id": "type"},
            {"name": "Trail", "id": "trail"},
            {"name": "Where", "id": "where"},
            {"name": "Notes", "id": "notes"},
            {"name": "Feel", "id": "feeling"},
    ]
    return columns


def main():
    df_empty = pd.DataFrame()

    runType_order = viz_constants.get_runType_order()
    runTypesToColors = viz_constants.get_runType_colors()
    runTypes_long_name = get_ordered_runType_long_name(runType_order)

    time_agg_options = get_time_options()

    #reading data
    df = read_pandas_pickle()

    year_marks = viz_constants.get_year_marks(df)
    available_cols = get_available_columns()

    filt_df = df.copy()

    encoded_image = base64.b64encode(open('img/logo.png', 'rb').read())

    #external_stylesheets = ['viz/data.css']
    #app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'height':'40px', 'display':'inline-block', 'margin':'5px 0px 0px 10px'}),
           html.H2("Running log - Activities", style={'display':'inline-block', 'vertical-align': 'center', 'margin':'0px', 'padding':'3px 0px 5px 20px'}) 
        ], style={'background-color':'#A4C1D9', 'height':'50px', 'vertical-align': 'center', 'padding':'0px', 'margin':'0px', 'margin-block-start':'0px', 'display':'flex'}),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Slider(
                        id='year-slider',
                        min=min(year_marks.keys()),
                        max=max(year_marks.keys()),
                        value=max(year_marks.keys())-1,
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
                            {'label': 'Mountaineering', 'value': 'X'},
                            {'label': 'Biking', 'value': 'XB'},
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
                        value='All',
                        labelStyle={'display': 'inline-block'}
                    )
                ], style={'display':'inline-block', 'vertical-align': 'top'})
            ], style={'width':'100%', 'display':'flex','justify-content':'space-around','padding-top':'5px'}),
            html.Hr(style={'margin':'0px 0px 10px 0px'}),

            html.Div(id='total_runs', style={'display': 'none'}), #hidden, in order to share data
            html.Div(id='last4weeks_agg', style={'display': 'none'}), #hidden, in order to share data
            html.Div(id='weekly_agg', style={'display': 'none'}), #hidden, in order to share data
            html.Div(id='monthly_agg', style={'display': 'none'}), #hidden, in order to share data
            html.Div(id='yearly_agg', style={'display': 'none'}), #hidden, in order to share data
            html.Div(id='agg_df', style={'display': 'none'}), #hidden, in order to share data

            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='yaxis-column2',
                            options=[{'label': i, 'value': i} for i in available_cols],
                            value='distance'
                        )
                    ], style={'width':'49%', 'display': 'inline-block', 'height':'30px'}),
                    html.Div([
                        dcc.Dropdown(
                            id='xaxis-column2',
                            options=[{'label': i, 'value': i} for i in time_agg_options],
                            value='week'
                        ),
                    ],style={'width':'50%', 'display': 'inline-block', 'height':'30px'}),
                    dcc.Graph(id='agg_graph') #graph!
                ],style={'display':'inline-block', 'width':'50%', 'float':'left', 'height':'380px'}),

                html.Div([
                    html.Div([html.H5("Last 4 weeks:"),],style={'height':'30px', 'textAlign':'center'}),
                    html.Div([
                        html.Div(
                            [dcc.Markdown(id='last_4weeks')], 
                        style={'white-space': 'pre', 'width':'400px', 'text-justify':'inter-word', 'display': 'inline-block', 'padding':'10px', 'border':'3px solid'}),
                     ], style={'text-align':'center'}),
                    html.Div([html.H5("Weekly summary:"),],style={'height':'30px', 'textAlign':'center'}),
                    html.Div([
                        dash_table.DataTable(
                            id='weekly_agg_table',
                            data=df_empty.to_dict('rows'),
                            columns=[{'id': c, 'name': c} for c in df_empty.columns],
                            style_table={
                                'overflowX': 'scroll', 
                                'maxHeight': '150px',
                                'overflowY': 'scroll'},
                            css=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }],
                            style_cell={
                                'whiteSpace': 'no-wrap',
                                #'whiteSpace': 'normal',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                #'textOverflow': 'clip',
                                'minWidth': '50px', 'maxWidth': '80px',
                                'font-size':'0.9em', 'font-family':'garamond',#georgia
                            },
                            style_as_list_view=True,
                            merge_duplicate_headers=True,
                            style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                },
                            #style_cell_conditional=[
                            #        {'if': {'column_id': 'week'}, 'width': '50px'},
                            #    ],
                            sort_action = 'native',
                            fixed_rows = { 'headers': True, 'data': 0 }
                        ),
                    ], style={'margin-right':'20px'})
                ], style={'width':'50%', 'display':'inline-block', 'height':'380px'}),
            ], style={'width':'100%', 'display':'block', 'height':'400px'}),
            html.Div([
                    html.Div([html.H5("All activities:"),],style={'height':'30px', 'textAlign':'center'}),
                    dash_table.DataTable(
                            id='total_runs_table',
                            data=df_empty.to_dict('rows'),
                            columns=[{'id': c, 'name': c} for c in df_empty.columns],
                            style_table={
                                'overflowX': 'scroll', 
                                'maxHeight': '250px',
                                'overflowY': 'scroll'},
                            css=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }],
                            style_cell={
                                'whiteSpace': 'no-wrap',
                                'overflow': 'hidden',
                                #'textOverflow': 'ellipsis',
                                'textOverflow': 'clip',
                                'font-size':'0.9em', 'font-family':'garamond',#georgia
                                'minWidth': '40px', 'maxWidth': '90px'
                            },
                            style_as_list_view=True,
                            merge_duplicate_headers=True,
                            style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                },
                            sort_action = 'native',
                            fixed_rows = { 'headers': True, 'data': 0 }
                        ),
            ], style={'width':'90%', 'display':'block','float':'center', 'padding-top':'10px', 'margin':'auto', 'border':'3px solid'}),
            html.Div([
                html.Div([
                    html.Div([html.H5("Monthly summary:"),],style={'height':'30px', 'textAlign':'center'}),
                    dash_table.DataTable(
                            id='monthly_agg_table',
                            data=df_empty.to_dict('rows'),
                            columns=[{'id': c, 'name': c} for c in df_empty.columns],
                            style_table={
                                'overflowX': 'scroll', 
                                'maxHeight': '150px',
                                'overflowY': 'scroll'},
                            css=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }],
                            style_cell={
                                'whiteSpace': 'no-wrap',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                'font-size':'0.9em', 'font-family':'garamond',#georgia
                                'minWidth': '20px', 'maxWidth': '80px'
                            },
                            style_as_list_view=True,
                            merge_duplicate_headers=True,
                            style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                },
                            sort_action = 'native',
                            fixed_rows = { 'headers': True, 'data': 0 }
                        ),
                ], style={'width':'45%', 'display':'inline-block'}),
                html.Div([
                    html.Div([html.H5("Yearly summary:"),],style={'height':'30px', 'textAlign':'center'}),
                    dash_table.DataTable(
                            id='yearly_agg_table',
                            data=df_empty.to_dict('rows'),
                            columns=[{'id': c, 'name': c} for c in df_empty.columns],
                            style_table={
                                'overflowX': 'scroll', 
                                'maxHeight': '150px',
                                'overflowY': 'scroll'},
                            css=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }],
                            style_cell={
                                'whiteSpace': 'no-wrap',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                'font-size':'0.9em', 'font-family':'garamond',#georgia
                                'minWidth': '20px', 'maxWidth': '80px'
                            },
                            style_as_list_view=True,
                            merge_duplicate_headers=True,
                            style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                },
                            sort_action = 'native',
                            fixed_rows = { 'headers': True, 'data': 0 }
                        ),
                ], style={'width':'45%', 'display':'inline-block'}),
            ], style={'width':'100%', 'display':'flex','justify-content':'space-around', 'height':'200px'}),
            html.Div([
                html.Div([html.H4("Evolution:")],style={'height':'40px', 'textAlign':'Left'}),
                html.Div([
                    dcc.Graph(id='graph_distr_dist', figure=update_distr_plot_figure(df,'distance', 'Dist. density', agg_all=True))
                ], style={'width':'33%', 'display':'inline-block', 'float':'left', 'margin':'auto'}),
                html.Div([
                    dcc.Graph(id='graph_distr_time', figure=update_distr_plot_figure(df,'time', 'Time density', agg_all=True))
                ], style={'width':'33%', 'display':'inline-block', 'margin':'auto'}),
                html.Div([
                    dcc.Graph(id='graph_distr_climb', figure=update_distr_plot_figure(df,'climb', 'Climb density', agg_all=True))
                ], style={'width':'33%', 'display':'inline-block', 'margin':'auto'}),
            ]),
            html.Div([html.H4("Top activities:"),],style={'height':'40px', 'textAlign':'Left'}),
            html.Div([
                html.Div([
                        html.Div([
                            html.Div([html.H6("Top distance:"),],style={'height':'30px', 'textAlign':'center'}),
                            dash_table.DataTable(
                                    id='top_long_activity_table',
                                    data=df_empty.to_dict('rows'),
                                    columns=record_table_columns(),
                                    style_table={
                                        'overflowX': 'scroll', 
                                        'maxHeight': '150px',
                                        'overflowY': 'scroll'},
                                    css=[{
                                            'selector': '.dash-cell div.dash-cell-value',
                                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                        }],
                                    style_cell={
                                        'whiteSpace': 'no-wrap',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'font-size':'0.9em', 'font-family':'garamond',#georgia
                                        'minWidth': '60px', 'maxWidth': '100px'
                                    },
                                    style_as_list_view=True,
                                    merge_duplicate_headers=True,
                                    style_header={
                                            'backgroundColor': 'white',
                                            'fontWeight': 'bold'
                                        },
                                    sort_action = 'native',
                                    fixed_rows = { 'headers': True, 'data': 0 }
                                ),
                            ],style={'display':'inline-block', 'width':'30%'}),
                        html.Div([
                            html.Div([html.H6("Top time:"),],style={'height':'30px', 'textAlign':'center'}),
                            dash_table.DataTable(
                                    id='top_time_activity_table',
                                    data=df_empty.to_dict('rows'),
                                    columns=record_table_columns(),
                                    style_table={
                                        'overflowX': 'scroll', 
                                        'maxHeight': '150px',
                                        'overflowY': 'scroll'},
                                    css=[{
                                            'selector': '.dash-cell div.dash-cell-value',
                                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                        }],
                                    style_cell={
                                        'whiteSpace': 'no-wrap',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'font-size':'0.9em', 'font-family':'garamond',#georgia
                                        'minWidth': '60px', 'maxWidth': '100px'
                                    },
                                    style_as_list_view=True,
                                    merge_duplicate_headers=True,
                                    style_header={
                                            'backgroundColor': 'white',
                                            'fontWeight': 'bold'
                                        },
                                    sort_action = 'native',
                                    fixed_rows = { 'headers': True, 'data': 0 }
                                ),
                            ],style={'display':'inline-block', 'width':'30%'}),
                        html.Div([
                            html.Div([html.H6("Top climb:"),],style={'height':'30px', 'textAlign':'center'}),
                            dash_table.DataTable(
                                    id='top_climb_activity_table',
                                    data=df_empty.to_dict('rows'),
                                    columns=record_table_columns(),
                                    style_table={
                                        'overflowX': 'scroll', 
                                        'maxHeight': '150px',
                                        'overflowY': 'scroll'},
                                    css=[{
                                            'selector': '.dash-cell div.dash-cell-value',
                                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                        }],
                                    style_cell={
                                        'whiteSpace': 'no-wrap',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'font-size':'0.9em', 'font-family':'garamond',#georgia
                                        'minWidth': '60px', 'maxWidth': '100px'
                                    },
                                    style_as_list_view=True,
                                    merge_duplicate_headers=True,
                                    style_header={
                                            'backgroundColor': 'white',
                                            'fontWeight': 'bold'
                                        },
                                    sort_action = 'native',
                                    fixed_rows = { 'headers': True, 'data': 0 }
                                ),
                            ],style={'display':'inline-block', 'width':'30%'}),
                ], style={'width':'100%', 'display':'flex','justify-content':'space-around', 'height':'200px'}),
                html.Div([
                        html.Div([
                            html.Div([html.H6("Top Vert. speed:"),],style={'height':'30px', 'textAlign':'center'}),
                            dash_table.DataTable(
                                    id='top_vspeed_activity_table',
                                    data=df_empty.to_dict('rows'),
                                    columns=record_table_columns(),
                                    style_table={
                                        'overflowX': 'scroll', 
                                        'maxHeight': '150px',
                                        'overflowY': 'scroll'},
                                    css=[{
                                            'selector': '.dash-cell div.dash-cell-value',
                                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                        }],
                                    style_cell={
                                        'whiteSpace': 'no-wrap',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'font-size':'0.9em', 'font-family':'garamond',#georgia
                                        'minWidth': '60px', 'maxWidth': '100px'
                                    },
                                    style_as_list_view=True,
                                    merge_duplicate_headers=True,
                                    style_header={
                                            'backgroundColor': 'white',
                                            'fontWeight': 'bold'
                                        },
                                    sort_action = 'native',
                                    fixed_rows = { 'headers': True, 'data': 0 }
                                ),
                            ],style={'display':'inline-block', 'width':'30%'}),
                        html.Div([
                            html.Div([html.H6("Top speed:"),],style={'height':'30px', 'textAlign':'center'}),
                            dash_table.DataTable(
                                    id='top_pace_activity_table',
                                    data=df_empty.to_dict('rows'),
                                    columns=record_table_columns(),
                                    style_table={
                                        'overflowX': 'scroll', 
                                        'maxHeight': '150px',
                                        'overflowY': 'scroll'},
                                    css=[{
                                            'selector': '.dash-cell div.dash-cell-value',
                                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                        }],
                                    style_cell={
                                        'whiteSpace': 'no-wrap',
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'font-size':'0.9em', 'font-family':'garamond',#georgia
                                        'minWidth': '60px', 'maxWidth': '100px'
                                    },
                                    style_as_list_view=True,
                                    merge_duplicate_headers=True,
                                    style_header={
                                            'backgroundColor': 'white',
                                            'fontWeight': 'bold'
                                        },
                                    sort_action = 'native',
                                    fixed_rows = { 'headers': True, 'data': 0 }
                                ),
                            ],style={'display':'inline-block', 'width':'30%'}),
                ], style={'width':'100%', 'display':'flex','justify-content':'space-around', 'height':'200px'}),
            ], style={'width':'90%', 'display':'block','float':'center', 'padding-top':'5px', 'margin':'auto', 'height':'400px'}),
            html.Div([html.H4("Location:"),],style={'height':'40px', 'textAlign':'Left'}),
            html.Div([
                html.Div([
                    dcc.Graph(id='freq_graph') #graph!
                ],style={'display':'inline-block', 'width':'49%', 'float':'left'}),
                html.Div([
                    html.Div([html.H5("Summary Statistics:"),],style={'height':'30px', 'textAlign':'center'}),
                    dash_table.DataTable(
                            id='summary_table',
                            data=df_empty.to_dict('rows'),
                            columns=[{'id': c, 'name': c} for c in df.columns],
                            style_table={
                                'overflowX': 'scroll', 
                                'maxHeight': '150px',
                                'overflowY': 'scroll'},
                            css=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }],
                            style_cell={
                                'whiteSpace': 'no-wrap',
                                'overflow': 'hidden',
                                'textOverflow': 'ellipsis',
                                'font-size':'0.9em', 'font-family':'garamond',#georgia
                                'minWidth': '60px', 'maxWidth': '100px'
                            },
                            style_as_list_view=True,
                            merge_duplicate_headers=True,
                            style_header={
                                    'backgroundColor': 'white',
                                    'fontWeight': 'bold'
                                },
                            sort_action = 'native',
                            fixed_rows = { 'headers': True, 'data': 0 }
                        ),
                ],style={'display':'inline-block', 'width':'49%', 'float':'right'}),
            ], style={'width':'90%', 'display':'block','float':'center', 'padding-top':'10px', 'margin':'auto', 'height':'300px'}),
        ], style={'margin-left':'8px'})
    ])

    @app.callback(
        dash.dependencies.Output('total_runs', 'children'),
        [dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value'),
        dash.dependencies.Input('year-slider', 'value')])
    def selected_runs(chosen_activities, trail_road_selector, chosen_year):
        if chosen_year == df.date.dt.year.max()+2:
            filt_df = df
        elif chosen_year == df.date.dt.year.max()+1:
            today = datetime.datetime.now()
            last_year = subtract_weeks(today, weeks=52)
            filt_df = df[np.logical_and(df.date >= last_year, df.date <= today)]
        else:
            filt_df = df[df.date.dt.year == chosen_year]

        return filt_df.to_json(date_format='iso', orient='split')

    @app.callback(
        dash.dependencies.Output('total_runs_table', 'data'),
        [dash.dependencies.Input('total_runs', 'children')])
    def update_figure(total_runs_json):
        df_total_runs = pd.read_json(total_runs_json, orient='split')

        df_total_runs['time'] = df_total_runs['time'].apply(lambda x: '{:d}h {:0>2d}m'.format(int(x//60), int(x%60)))
        df_total_runs['avg_pace'] = df_total_runs['avg_pace'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        df_total_runs['paceE'] = df_total_runs['paceE'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        df_total_runs['paceM'] = df_total_runs['paceM'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        df_total_runs['paceT'] = df_total_runs['paceT'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        df_total_runs['paceI'] = df_total_runs['paceI'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        df_total_runs['paceR'] = df_total_runs['paceR'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))

        #df_total_runs.date = df_total_runs.date.dt.strftime("%d-%m-%y")
        df_total_runs.date = df_total_runs.date.apply(lambda x: x.strftime("%y-%m-%d"))

        decimals = pd.Series([1, 1, 0, 1, 1, 1, 1, 1], index=['distance', 'time', 'climb', 'distE', 'distM', 'distT', 'distI', 'distR'])
        return df_total_runs.round(decimals).sort_values(by=['date'], ascending=False).to_dict('rows')

    @app.callback(
        dash.dependencies.Output('total_runs_table', 'columns'),
        [dash.dependencies.Input('total_runs', 'children')])
    def update_figure(df_agg_json): #TODO: df_agg_json can be removed
        columns=[
                {"name": "Date", "id": "date"},
                {"name": "Type", "id": "type"},
                {"name": "Trail", "id": "trail"},
                {"name": "Dist.", "id": "distance"},
                {"name": "Time", "id": "time"},
                {"name": "Climb", "id": "climb"},
                {"name": "V.Speed", "id": "vspeed"},
                {"name": "Avg.Pace", "id": "avg_pace"},
                {"name": "Where", "id": "where"},
                {"name": "Route", "id": "route"},
                {"name": "Notes", "id": "notes"},
                {"name": "Feel", "id": "feeling"},
                {"name": "Dist.E", "id": "distE"},
                {"name": "Dist.M", "id": "distM"},
                {"name": "Dist.T", "id": "distT"},
                {"name": "Dist.I", "id": "distI"},
                {"name": "Dist.R", "id": "distR"},
                {"name": "Pace.E", "id": "paceE"},
                {"name": "Pace.M", "id": "paceM"},
                {"name": "Pace.T", "id": "paceT"},
                {"name": "Pace.I", "id": "paceI"},
                {"name": "Pace.R", "id": "paceR"},
            ]
        return columns

    @app.callback(
        dash.dependencies.Output('agg_df', 'children'),
        [dash.dependencies.Input('xaxis-column2', 'value'),
        dash.dependencies.Input('yaxis-column2', 'value'),
        dash.dependencies.Input('weekly_agg', 'children'),
        dash.dependencies.Input('monthly_agg', 'children'),
        dash.dependencies.Input('yearly_agg', 'children'),
        dash.dependencies.Input('year-slider', 'value')]
    )
    def agg_data(xaxis_colname, yaxis_colname,
            df_w_agg, df_m_agg, df_y_agg, chosen_year):

        if xaxis_colname == 'week':
            filt_df = pd.read_json(df_w_agg, orient='split')
        elif xaxis_colname == 'month':
            filt_df = pd.read_json(df_m_agg, orient='split')
        elif xaxis_colname == 'year':
            filt_df = pd.read_json(df_y_agg, orient='split')

        filt_df['date'] = filt_df.index


        if chosen_year == df.date.dt.year.max()+2:
            pass #do nothing
        elif chosen_year == df.date.dt.year.max()+1:
            today = datetime.datetime.now()
            last_year = subtract_weeks(today, 52)
            filt_df = filt_df[np.logical_and(filt_df.date >= last_year, filt_df.date <= today)]
        else:
            filt_df = filt_df[filt_df.date.dt.year == chosen_year]


        return filt_df.to_json(date_format='iso', orient='split')

    def time_aggregate(df, chosen_activities, trail_road_selector, time_option=''):
        if time_option == 'week':
            agg_option = 'W'
        elif time_option == 'month':
            agg_option = 'MS'
        elif time_option == 'year':
            agg_option = 'YS'
        elif time_option == 'all':
            agg_option = '2Y'
        else:
            agg_option = 'W'

        chosen_activity_types = viz_constants.get_activities_from_checklist(chosen_activities)
        filt_df = df[df.type.isin(chosen_activity_types)]

        trail_road = viz_constants.get_trail_road_activities(trail_road_selector)
        filt_df = filt_df[filt_df.trail.isin(trail_road)]

        if filt_df.shape[0] == 0:
            cols = list(filt_df.columns)
            cols.extend(['N_run', 'N_trail', 'N_all', 'Nall_Nroad_Ntrail', 'run_avg_pace', '%E','%M','%T','%I','%R', '%types'])
            data = [0]*len(cols)
            return pd.DataFrame(columns = cols, data = [data]).to_json(date_format='iso', orient='split')
        #END apply filters




        needed_cols = ['date', 'distance', 'time', 'climb', 'distE', 'distI', 'distM', 'distR', 'distT', 'distX', 'distXB', 'timeE', 'timeI', 'timeM', 'timeR', 'timeT', 'timeX', 'timeXB']
        df_agg = filt_df[:][needed_cols].resample(agg_option, on='date').agg(pd.Series.sum, skipna=True)

        agg_feeling = filt_df[:][['date', 'feeling']].resample(agg_option, on='date').agg(pd.Series.mean, skipna=True)
        df_agg = pd.concat([df_agg, agg_feeling], axis=1, sort=False)

        #Count all activities
        df_count_all = filt_df[:][['date']].resample(agg_option, on='date').agg({'date':'size'}).rename(columns={'date':'N_all'})
        df_agg = pd.concat([df_agg, df_count_all], axis=1, sort=False)


        #count road/trail #runs and distance
        df_running = filt_df[filt_df.type.isin(runTypes.RUNNING_ACTIVITIES)][['date', 'distance', 'trail']]
        df_running.trail = df_running.trail.astype('int')
        df_running.reset_index(drop=True, inplace=True)
        df_running = df_running.groupby('trail').resample(agg_option, on='date').agg({'distance':'sum', 'trail':'size'})
        df_running.rename(index={0:'road',1:'trail'}, columns={'trail':'n'},inplace=True)
        df_running = df_running.unstack('trail', fill_value=0)
        df_running.columns = ['_'.join(col).strip() for col in df_running.columns.values]
        for col in ['distance_road', 'distance_trail', 'n_road', 'n_trail']:
            if col not in df_running.columns:
                df_running[col] = 0

        df_agg = pd.concat([df_agg, df_running], axis=1, sort=False)

        cols = ['n_road', 'n_trail', 'N_all']
        df_agg['Nall_Nroad_Ntrail'] = df_agg[cols].apply(lambda row: "%d/%.0f/%.0f"%(row.values[2],row.values[0],row.values[1]), axis=1)



        df_agg[time_option] = df_agg.index
        if time_option == 'week':
            pattern = '%Y-%m-%d'
        elif time_option == 'month':
            pattern = '%Y-%m'
        elif time_option == 'year':
            pattern = '%Y'
        elif time_option == 'all':
            pattern = '%Y'

        df_agg[time_option] = df_agg[time_option].apply(lambda x: x.strftime(pattern))

        #avg pace all activities
        df_agg['avg_pace'] = df_agg['time']*60/df_agg['distance']

        #avg pace all activities
        df_agg['vspeed'] = df_agg['climb']*60./df_agg['time']
        df_agg.loc[df_agg['time'] == 0, 'vspeed'] = 0
        df_agg.vspeed.astype('int')

        #running avg pace
        df_agg_notX = filt_df[filt_df.type.isin(runTypes.RUNNING_ACTIVITIES)][needed_cols].resample(agg_option, on='date').sum()
        df_agg_notX['run_avg_pace'] = df_agg_notX['time']*60/df_agg_notX['distance']

        df_agg = pd.concat([df_agg, df_agg_notX['run_avg_pace']], axis=1)

        df_agg['%E'] = 100*df_agg['distE'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])
        df_agg['%M'] = 100*df_agg['distM'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])
        df_agg['%T'] = 100*df_agg['distT'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])
        df_agg['%I'] = 100*df_agg['distI'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])
        df_agg['%R'] = 100*df_agg['distR'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])
        df_agg['%X'] = df_agg['%XB'] = 0

        df_agg.fillna(value={'%E':0, '%M':0, '%T':0, '%I':0, '%R':0}, inplace=True)

        cols = ['%E','%M','%T','%I','%R']
        df_agg['%types'] = df_agg[cols].apply(lambda row: "%.0f(%.0f)%%/%.0f%%/%.0f%%/%.0f%%"%(row.values[0]+row.values[1],row.values[1],row.values[2],row.values[3],row.values[4]), axis=1)

        decimals = pd.Series([1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0], index=['distance', 'time', 'climb', 'run_avg_pace', '%E', '%M', '%T', '%I', '%R', 'feeling', 'vspeed'])

        return df_agg.round(decimals).to_json(date_format='iso', orient='split')

    @app.callback(
        dash.dependencies.Output('weekly_agg', 'children'),
        [dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value')]
    )
    def weekly_summary(chosen_activities, trail_road_selector):
        return time_aggregate(df, chosen_activities, trail_road_selector, 'week')

    @app.callback(
        dash.dependencies.Output('weekly_agg_table', 'data'),
        [dash.dependencies.Input('weekly_agg', 'children')])
    def update_figure(df_agg_json):
        df_agg = pd.read_json(df_agg_json, orient='split')

        df_agg['time'] = df_agg['time'].apply(lambda x: '{:d}h {:0>2d}m'.format(int(x//60), int(x%60)))
        df_agg['run_avg_pace'] = df_agg['run_avg_pace'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))

        return df_agg.sort_values(by=['week'], ascending=False).to_dict('rows')

    @app.callback(
        dash.dependencies.Output('weekly_agg_table', 'columns'),
        [dash.dependencies.Input('weekly_agg', 'children')])
    def update_figure(df_agg_json):
        columns=[
                {"name": "Week", "id": "week"},
                {"name": "Dist.", "id": "distance"},
                {"name": "Time", "id": "time"},
                {"name": "Climb", "id": "climb"},
                {"name": "V.Speed", "id": "vspeed"},
                {"name": "Pace", "id": "run_avg_pace"},
                {"name": "E(M)%/T%/I%/R%", "id": "%types"},
                {"name": "Feel", "id": "feeling"},
                {"name": "#A/#R/#T", "id": "Nall_Nroad_Ntrail"},
            ]
        return columns

    @app.callback(
        dash.dependencies.Output('monthly_agg', 'children'),
        [dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value')]
    )
    def monthly_summary(chosen_activities, trail_road_selector):
        return time_aggregate(df, chosen_activities, trail_road_selector, 'month')

    @app.callback(
        dash.dependencies.Output('monthly_agg_table', 'data'),
        [dash.dependencies.Input('monthly_agg', 'children')])
    def update_figure(df_agg_json):
        df_agg = pd.read_json(df_agg_json, orient='split')

        df_agg['time'] = df_agg['time'].apply(lambda x: '{:d}h {:0>2d}m'.format(int(x//60), int(x%60)))
        df_agg['run_avg_pace'] = df_agg['run_avg_pace'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))

        return df_agg.sort_values(by=['month'], ascending=False).to_dict('rows')

    @app.callback(
        dash.dependencies.Output('monthly_agg_table', 'columns'),
        [dash.dependencies.Input('monthly_agg', 'children')])
    def update_figure(df_agg_json):
        columns=[
                {"name": "Month", "id": "month"},
                {"name": "Dist.", "id": "distance"},
                {"name": "Time", "id": "time"},
                {"name": "Climb", "id": "climb"},
                {"name": "V.Speed", "id": "vspeed"},
                {"name": "Run.Avg.Pace", "id": "run_avg_pace"},
                {"name": "E(M)%/T%/I%/R%", "id": "%types"},
                {"name": "Feel", "id": "feeling"},
                {"name": "#A/#R/#T", "id": "Nall_Nroad_Ntrail"},
            ]
        return columns

    @app.callback(
        dash.dependencies.Output('yearly_agg', 'children'),
        [dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value')]
    )
    def yearly_summary(chosen_activities, trail_road_selector):
        return time_aggregate(df, chosen_activities, trail_road_selector, 'year')

    @app.callback(
        dash.dependencies.Output('yearly_agg_table', 'data'),
        [dash.dependencies.Input('yearly_agg', 'children')])
    def update_figure(df_agg_json):
        df_agg = pd.read_json(df_agg_json, orient='split')

        df_agg['time'] = df_agg['time'].apply(lambda x: '{:d}h {:0>2d}m'.format(int(x//60), int(x%60)))
        df_agg['run_avg_pace'] = df_agg['run_avg_pace'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))

        return df_agg.sort_values(by=['year'],ascending=False).to_dict('rows')

    @app.callback(
        dash.dependencies.Output('yearly_agg_table', 'columns'),
        [dash.dependencies.Input('yearly_agg', 'children')])
    def update_figure(df_agg_json):
        columns=[
                {"name": "Year", "id": "year"},
                {"name": "Dist.", "id": "distance"},
                {"name": "Time", "id": "time"},
                {"name": "Climb", "id": "climb"},
                {"name": "V.Speed", "id": "vspeed"},
                {"name": "Run.Avg.Pace", "id": "run_avg_pace"},
                {"name": "E(M)%/T%/I%/R%", "id": "%types"},
                {"name": "Feel", "id": "feeling"},
                {"name": "#A/#R/#T", "id": "Nall_Nroad_Ntrail"},
            ]
        return columns

    @app.callback(
        dash.dependencies.Output('agg_graph', 'figure'),
        [dash.dependencies.Input('xaxis-column2', 'value'),
         dash.dependencies.Input('yaxis-column2', 'value'),
         dash.dependencies.Input('chosen_types', 'value'),
         dash.dependencies.Input('trail_road_selector', 'value'),
         dash.dependencies.Input('agg_df', 'children')])
    def update_figure(xaxis_colname, yaxis_colname, chosen_activities, trail_road_selector, df_agg_json):
        df_agg = pd.read_json(df_agg_json, orient='split')

        xaxis_dict = {'title':xaxis_colname}
        yaxis_dict = {'title':yaxis_colname}


        if xaxis_colname == 'day':
            xaxis_colname = 'date'

        if yaxis_colname in ('distance', 'time', '%types'):
            if yaxis_colname == 'distance':
                str_template = 'dist%s'
            elif yaxis_colname == 'time':
                str_template = 'time%s'
            elif yaxis_colname == '%types':
                str_template = '%%%s'

            traces = [
                go.Bar(
                    x=df_agg[:][xaxis_colname],
                    y=df_agg[:][str_template%i],
                    opacity=0.5,
                    hovertext = df_agg[:][yaxis_colname],
                    marker={ 'color': runTypesToColors[i] },
                    name=i
                ) for i in runTypes.BASIC_RUN_TYPES + runTypes.NON_RUNNING_ACTIVITIES
            ]
        elif yaxis_colname in ('distance road vs trail'):
            str_template = 'distance_%s'
            types = ['road', 'trail']
            colors = {'road':'#5557a6', 'trail':'#10931c'}
            traces = [
                go.Bar(
                    x=df_agg[:][xaxis_colname],
                    y=df_agg[:][str_template%i],
                    opacity=0.5,
                    hovertext = df_agg[:]['distance'],
                    marker={ 'color': colors[i] },
                    name=i
                ) for i in types
            ]
        else:
            traces = [
                go.Bar(
                    x=df_agg[:][xaxis_colname],
                    y=df_agg[:][yaxis_colname],
                    opacity=0.5,
                    marker={ 'color': '#1f77b4' },
                    name='All'
                ) 
            ]

        return {
            'data': traces,
            'layout': go.Layout(
                height=350,
                #width=600,
                barmode='stack',
                xaxis=xaxis_dict,
                yaxis=yaxis_dict,
                bargap=0.05,
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                #legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }

    @app.callback(
        dash.dependencies.Output('freq_graph', 'figure'),
        [dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value'),
        dash.dependencies.Input('year-slider', 'value')]
    )
    def update_figure(chosen_activities, trail_road_selector, chosen_year):
        #Apply filters
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

        column='where'
        counts = get_running_location_count(filt_df, column)
        counts = counts.nlargest(10, 'counts')[::-1]

        traces = [
            go.Bar(
                y=counts.index,
                x=counts.counts,
                opacity=0.90,
                marker={ 'color': '#A4C1D9' },
                name='All',
                orientation='h'
            ) 
        ]

        return {
            'data': traces,
            'layout': go.Layout(
                height=300,
                barmode='stack',
                yaxis={'title':'location'},
                xaxis={'title': 'counts'},
                bargap=0.05,
                margin={'l': 150, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }

    @app.callback(
        dash.dependencies.Output('last4weeks_agg', 'children'),
        [dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value')])
    def update_last4weeks_df(chosen_activities, trail_road_selector):
        #consider last 28 days (starting today)
        first_date = pd.Timestamp((pd.Timestamp.now() - datetime.timedelta(days=28)).date())
        df_slice = df[df['date'] > first_date]
        return time_aggregate(df_slice, chosen_activities, trail_road_selector, 'all')

    @app.callback(
        dash.dependencies.Output(component_id='last_4weeks', component_property='children'),
        [dash.dependencies.Input('last4weeks_agg', 'children')])
    def update_output_div(df_agg):
        agg = pd.read_json(df_agg, orient='split').iloc[0]

        avg_time = '{:d}h {:0>2d}m'.format(int(agg.time/4.//60),int(agg.time/4.%60))
        avg_pace = "{:d}:{:0>2d}".format(int(agg.avg_pace//60),int(agg.avg_pace%60))
        return '**Avg. distance:** {:.1f} km    **Avg. time:** {};\n'\
                '**Avg.pace:** {} min/km    **Avg. vert. speed:** {} m/h\n'\
                '**#Activities _All/Road/Trail_:**{}    **Avg. feel:** {} \n'\
                '**Distance _E(M)%/T%/I%/R%_:** {}'.format(agg.distance/4, 
                                                                                    avg_time, 
                                                                                    avg_pace, 
                                                                                    agg.vspeed, 
                                                                                    agg.Nall_Nroad_Ntrail, 
                                                                                    agg.feeling, 
                                                                                    agg['%types'])
    #@app.callback(
    #    dash.dependencies.Output(component_id='last_4weeks', component_property='children'),
    #    [dash.dependencies.Input('chosen_types', 'value')])
    #def update_output_div(chosen_activities):
    #    #consider last 28 days (starting today)
    #    first_date = pd.Timestamp((pd.Timestamp.now() - datetime.timedelta(days=28)).date())
    #    df_slice = df[df['date'] > first_date]
    #    df_agg_json = time_aggregate(df_slice, chosen_activities, 'all')
    #    agg = pd.read_json(df_agg_json, orient='split').iloc[0]

    #    avg_time = '{:d}h {:0>2d}m'.format(int(agg.time/4.//60),int(agg.time/4.%60))
    #    avg_pace = "{:d}:{:0>2d}".format(int(agg.avg_pace//60),int(agg.avg_pace%60))
    #    return '**Avg. distance:** {:.1f} km;    **Avg. time:** {};\n'\
    #            '**Avg.pace:** {} min/km;    **Avg. vert. speed:** {} m/h\n'\
    #            '**#Activities _Run(Trail)/All_:**{};    **Avg. feel:** {} \n'\
    #            '**Distance _E(M)%_/_T%_/_I%_/_R%_:** {}'.format(agg.distance/4, 
    #                                                                                avg_time, 
    #                                                                                avg_pace, 
    #                                                                                agg.vspeed, 
    #                                                                                agg.Nall_Nroad_Ntrail, 
    #                                                                                agg.feeling, 
    #                                                                                agg['%types'])

    @app.callback(
        dash.dependencies.Output('summary_table', 'data'),
        [
        dash.dependencies.Input('weekly_agg', 'children'),
        dash.dependencies.Input('monthly_agg', 'children'),
        dash.dependencies.Input('yearly_agg', 'children')
        ])
    def update_figure(weekly_agg_json, monthly_agg_json, yearly_agg_json):
        w_agg = pd.read_json(weekly_agg_json, orient='split')
        m_agg = pd.read_json(monthly_agg_json, orient='split')
        y_agg = pd.read_json(yearly_agg_json, orient='split')

        index = ['4W', 'W', 'M', 'Y']
        columns = ['avg_dist', 'sd_dist', 'avg_time', 'sd_time', 'avg_climb', 'sd_climb', 'avg_N_run', 'sd_N_run', 'avg_N_trail', 'sd_N_trail', 'avg_N_all', 'sd_N_all']
        summary_df = pd.DataFrame(index=index, columns=columns)

        aggs = [w_agg.iloc[-5:-1], w_agg[:-1], m_agg.iloc[:-1], y_agg]
        variables = ['distance', 'time', 'climb', 'n_road', 'n_trail', 'N_all']
        for i in range(4):
            df_agg = aggs[i]
            metrics = []
            for var in variables:
                stats = np.around([df_agg[var].mean(), df_agg[var].std()],1)
                vf = np.vectorize(lambda x: "-" if np.isnan(x) else '{:d}h {:0>2d}m'.format(int(x//60),int(x%60)))
                if var == 'time':
                    stats = vf(stats)
                metrics.extend(stats)
            summary_df.iloc[i] = metrics

        cols = ['avg_N_run', 'avg_N_trail', 'avg_N_all']
        summary_df['N_avg'] = summary_df[cols].apply(lambda row: "%.1f(%.1f)/%.1f"%(row.values[0],row.values[1],row.values[2]), axis=1)

        summary_df['period'] = ['Last 4 W', 'Week', 'Month', 'Year']
        return summary_df.to_dict('rows')

    @app.callback(
        dash.dependencies.Output('summary_table', 'columns'),
        [
        dash.dependencies.Input('weekly_agg', 'children'),
        dash.dependencies.Input('monthly_agg', 'children'),
        dash.dependencies.Input('yearly_agg', 'children')
        ])
    def update_figure(weekly_agg_json, monthly_agg_json, yearly_agg_json):
        columns=[
                {"name": "Period", "id": "period"},
                {"name": "Dist.Avg", "id": "avg_dist"},
                {"name": "Dist.SD", "id": "sd_dist"},
                {"name": "Time.Avg", "id": "avg_time"},
                {"name": "Time.SD", "id": "sd_time"},
                {"name": "Climb.Avg", "id": "avg_climb"},
                {"name": "Clim.SD", "id": "sd_climb"},
                {"name": "#Run.Avg", "id": "N_avg"},
            ]
        return columns


    def return_top_values(df, column, n, ascending=False):
        return df.sort_values(by=column,ascending=ascending).iloc[0:n]

    @app.callback(
        dash.dependencies.Output('top_long_activity_table', 'data'),
        [dash.dependencies.Input('total_runs', 'children'),
        dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value')])
    def record_table(df_json, chosen_activities, trail_road_selector):
        df = pd.read_json(df_json, orient='split')

        chosen_activity_types = viz_constants.get_activities_from_checklist(chosen_activities)
        df = df[df.type.isin(chosen_activity_types)]

        trail_road = viz_constants.get_trail_road_activities(trail_road_selector)
        df = df[df.trail.isin(trail_road)]

        df.date = df.date.apply(lambda x: x.strftime("%y/%m/%d"))
        df['avg_pace'] = df['avg_pace'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        decimals = pd.Series([1, 1, 0, 1, 1, 1, 1, 1, 1], index=['distance', 'time', 'climb', 'distE', 'distM', 'distT', 'distI', 'distR', 'feel'])
        return return_top_values(df.round(decimals), 'distance', 10).to_dict('rows')

    @app.callback(
        dash.dependencies.Output('top_time_activity_table', 'data'),
        [dash.dependencies.Input('total_runs', 'children'),
        dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value')])
    def record_table(df_json, chosen_activities, trail_road_selector):
        df = pd.read_json(df_json, orient='split')

        chosen_activity_types = viz_constants.get_activities_from_checklist(chosen_activities)
        df = df[df.type.isin(chosen_activity_types)]

        trail_road = viz_constants.get_trail_road_activities(trail_road_selector)
        df = df[df.trail.isin(trail_road)]

        df.date = df.date.apply(lambda x: x.strftime("%y/%m/%d"))
        df['avg_pace'] = df['avg_pace'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        decimals = pd.Series([1, 1, 0, 1, 1, 1, 1, 1, 1], index=['distance', 'time', 'climb', 'distE', 'distM', 'distT', 'distI', 'distR', 'feel'])
        return return_top_values(df.round(decimals), 'time', 10).to_dict('rows')

    @app.callback(
        dash.dependencies.Output('top_vspeed_activity_table', 'data'),
        [dash.dependencies.Input('total_runs', 'children'),
        dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value')])
    def record_table(df_json, chosen_activities, trail_road_selector):
        df = pd.read_json(df_json, orient='split')

        chosen_activity_types = viz_constants.get_activities_from_checklist(chosen_activities)
        df = df[df.type.isin(chosen_activity_types)]

        trail_road = viz_constants.get_trail_road_activities(trail_road_selector)
        df = df[df.trail.isin(trail_road)]

        df.date = df.date.apply(lambda x: x.strftime("%y/%m/%d"))
        df['avg_pace'] = df['vspeed'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        decimals = pd.Series([1, 1, 0, 1, 1, 1, 1, 1, 1], index=['distance', 'time', 'climb', 'distE', 'distM', 'distT', 'distI', 'distR', 'feel'])
        return return_top_values(df.round(decimals), 'vspeed', 10).to_dict('rows')

    @app.callback(
        dash.dependencies.Output('top_climb_activity_table', 'data'),
        [dash.dependencies.Input('total_runs', 'children'),
        dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value')])
    def record_table(df_json, chosen_activities, trail_road_selector):
        df = pd.read_json(df_json, orient='split')

        chosen_activity_types = viz_constants.get_activities_from_checklist(chosen_activities)
        df = df[df.type.isin(chosen_activity_types)]

        trail_road = viz_constants.get_trail_road_activities(trail_road_selector)
        df = df[df.trail.isin(trail_road)]

        df.date = df.date.apply(lambda x: x.strftime("%y/%m/%d"))
        df['avg_pace'] = df['vspeed'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        decimals = pd.Series([1, 1, 0, 1, 1, 1, 1, 1, 1], index=['distance', 'time', 'climb', 'distE', 'distM', 'distT', 'distI', 'distR', 'feel'])
        return return_top_values(df.round(decimals), 'climb', 10).to_dict('rows')

    @app.callback(
        dash.dependencies.Output('top_pace_activity_table', 'data'),
        [dash.dependencies.Input('total_runs', 'children'),
        dash.dependencies.Input('chosen_types', 'value'),
        dash.dependencies.Input('trail_road_selector', 'value')])
    def record_table(df_json, chosen_activities, trail_road_selector):
        df = pd.read_json(df_json, orient='split')

        chosen_activity_types = viz_constants.get_activities_from_checklist(chosen_activities)
        df = df[df.type.isin(chosen_activity_types)]

        trail_road = viz_constants.get_trail_road_activities(trail_road_selector)
        df = df[df.trail.isin(trail_road)]

        df.date = df.date.apply(lambda x: x.strftime("%y/%m/%d"))
        decimals = pd.Series([1, 1, 0, 1, 1, 1, 1, 1, 1], index=['distance', 'time', 'climb', 'distE', 'distM', 'distT', 'distI', 'distR', 'feel'])
        df_pace = return_top_values(df.round(decimals), 'avg_pace', 10, ascending=True)
        df_pace['avg_pace'] = df_pace['avg_pace'].apply(lambda x: "-" if np.isnan(x) else "{:d}:{:0>2d}".format(int(x//60),int(x%60)))
        return df_pace.to_dict('rows')



    return app

if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
