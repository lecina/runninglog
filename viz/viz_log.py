import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from plotly.tools import FigureFactory as ff
import seaborn as sns
import matplotlib.pyplot as plt
import dash_table
import datetime

import pandas as pd
import numpy as np

from constants import blockNames
from viz.viz_constants import viz_constants

def read_pandas_pickle(fname = "data/processed/df.pkl"):
    df = pd.read_pickle(fname)
    df.date = pd.to_datetime(df.date)
    return df

def get_year_marks(df):
    years = df.date.dt.year
    year_marks={year: str(year) for year in np.hstack([years.unique(), [years.max()+1], [years.max()+2]])}
    year_marks[years.max()+1] = 'Last year'
    year_marks[years.max()+2] = 'All'

    return year_marks


def get_basic_runTypes_order():
    runType_order = [blockNames.RunTypes.E, 
                     blockNames.RunTypes.M,
                     blockNames.RunTypes.T,
                     blockNames.RunTypes.I,
                     blockNames.RunTypes.R,
                     blockNames.RunTypes.X,
                     blockNames.RunTypes.XB]
    return runType_order

def get_ordered_runType_long_name(runType_order):
    return [{'value':rt, 'label':blockNames.RUN_TYPES_LONG_NAME_DICTIONARY[rt] } for rt in runType_order]

def get_available_columns():
    available_cols = ['distance', 'time', 'climb', 'avg_pace', 'run_avg_pace', '%types']
    return available_cols

def get_time_options():
    time_agg_options = ['', 'day', 'week', 'month', 'year']
    return time_agg_options

def get_running_location_count(df):
    counts = pd.crosstab(index=df['where'], columns="count") 
    rel_counts = counts/counts.sum()*100
    counts = pd.concat([counts, rel_counts], axis=1)
    counts.columns = ['counts','rel_counts']
    return counts

def subtract_weeks(d, weeks=52):
    return d - datetime.timedelta(days=d.weekday() + 7*weeks)

def main():
    basic_runType_order = get_basic_runTypes_order()

    runType_order = viz_constants.get_runType_order()
    runTypesToColors = viz_constants.get_runType_colors()
    runTypes_long_name = get_ordered_runType_long_name(runType_order)

    time_agg_options = get_time_options()

    #reading data
    df = read_pandas_pickle()

    year_marks = get_year_marks(df)
    available_cols = get_available_columns()

    filt_df = df.copy()

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
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
            ], style={'width': '30%', 'display': 'inline-block', 'padding': '0px 0px 0px 0px'}),
            html.Div([
                dcc.Dropdown(
                    id='type-dropdown',
                    options=runTypes_long_name,
                    value=[blockNames.RunTypes.XB, blockNames.RunTypes.X, blockNames.RunTypes.C, blockNames.RunTypes.R, blockNames.RunTypes.I, blockNames.RunTypes.T, blockNames.RunTypes.M, blockNames.RunTypes.E],
                    multi = True
                )
            ], style={
                            'width': '70%',
                            'float': 'right',
                            'display': 'inline-block',
                            'align-items': 'center',
                            'padding': '0px 0px 0px 0px'
                        })
        ]),
        html.Div(id='total_runs', style={'display': 'none'}), #hidden, in order to share data
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
                ],style={'width':'49%', 'display': 'inline-block', 'height':'30px'}),
                dcc.Graph(id='agg_graph') #graph!
            ],style={'display':'inline-block', 'width':'49%', 'float':'left', 'height':'330px'}),
            #display:flex;justify-content:center;align-items:center

            html.Div([
                html.Div([html.H5("Weekly summary:"),],style={'height':'30px', 'textAlign':'center'}),
                dash_table.DataTable(
                    id='weekly_agg_table',
                    data=df[0:0].to_dict('rows'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    style_table={
                        'overflowX': 'scroll', 
                        'maxHeight': '280px',
                        'overflowY': 'scroll'},
                    css=[{
                            'selector': '.dash-cell div.dash-cell-value',
                            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                        }],
                    style_cell={
                        'whiteSpace': 'no-wrap',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
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
            ], style={'width':'49%', 'display':'inline-block', 'height':'330px'}),
        ], style={'width':'100%', 'display':'block', 'height':'350px'}),
        html.Div([
                html.Div([html.H5("All activities:"),],style={'height':'30px', 'textAlign':'center'}),
                dash_table.DataTable(
                        id='total_runs_table',
                        data=df[0:0].to_dict('rows'),
                        columns=[{'id': c, 'name': c} for c in df.columns],
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
                            'textOverflow': 'ellipsis',
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
        ], style={'width':'90%', 'display':'block','float':'center', 'padding-top':'10px', 'margin':'auto', 'border':'3px solid'}),
        html.Div([
            html.Div([html.H5("Monthly summary:"),],style={'height':'30px', 'textAlign':'center'}),
            dash_table.DataTable(
                    id='monthly_agg_table',
                    data=df[0:0].to_dict('rows'),
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
        ], style={'width':'49%', 'display':'inline-block','justify-content':'center','align-items':'center', 'float':'left', 'padding-top':'10px', 'height':'200px'}),
        html.Div([
            html.Div([html.H5("Yearly summary:"),],style={'height':'30px', 'textAlign':'center'}),
            dash_table.DataTable(
                    id='yearly_agg_table',
                    data=df[0:0].to_dict('rows'),
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
        ], style={'width':'49%', 'display':'inline-block','justify-content':'center','align-items':'center', 'padding-top':'10px', 'height':'200px'}),
        html.Div([
            dcc.Graph(id='freq_graph') #graph!
        ],style={'display':'inline-block', 'width':'49%', 'float':'left', 'height':'330px'}),
        html.Div([
            html.Div([html.H5("Statistics:"),],style={'height':'30px', 'textAlign':'center'}),
            dash_table.DataTable(
                    id='summary_table',
                    data=df[0:0].to_dict('rows'),
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
        ],style={'display':'inline-block', 'width':'49%', 'float':'right', 'height':'330px'}),
        #], style={'width':'49%', 'display':'inline-block','justify-content':'center','align-items':'center', 'height':'330px'}),
    ])

    @app.callback(
        dash.dependencies.Output('total_runs', 'children'),
        [dash.dependencies.Input('type-dropdown', 'value'),
        dash.dependencies.Input('year-slider', 'value')])
    def selected_runs(chosen_basic_runTypes, chosen_year):
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
        decimals = pd.Series([1, 1, 0, 1, 1, 1, 1, 1], index=['distance', 'time', 'climb', 'distE', 'distM', 'distT', 'distI', 'distR'])

        #df_total_runs.date = df_total_runs.date.dt.strftime("%d-%m-%y")
        df_total_runs.date = df_total_runs.date.apply(lambda x: x.strftime("%y/%m/%d"))
        return df_total_runs.round(decimals).sort_values(by=['date'], ascending=False).to_dict('rows')

    @app.callback(
        dash.dependencies.Output('total_runs_table', 'columns'),
        [dash.dependencies.Input('total_runs', 'children')])
    def update_figure(df_agg_json):
        columns=[
                {"name": "Date", "id": "date"},
                {"name": "Type", "id": "type"},
                {"name": "Trail", "id": "trail"},
                {"name": "Dist.", "id": "distance"},
                {"name": "Time", "id": "time"},
                {"name": "Climb", "id": "climb"},
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

    def time_aggregate(chosen_basic_runTypes, time_option):
        if time_option == 'week':
            agg_option = 'W'
        elif time_option == 'month':
            agg_option = 'MS'
        elif time_option == 'year':
            agg_option = 'YS'
        else:
            agg_option = 'W'

        filt_df = df[df.type.isin(chosen_basic_runTypes)]
        #END apply filters


        needed_cols = ['date', 'distance', 'time', 'climb', 'distE', 'distI', 'distM', 'distR', 'distT', 'distX', 'distXB', 'timeE', 'timeI', 'timeM', 'timeR', 'timeT', 'timeX', 'timeXB']
        df_agg = filt_df[:][needed_cols].resample(agg_option, on='date').sum()

        df_agg[time_option] = df_agg.index
        if time_option == 'week':
            pattern = '%Y-%m-%d'
        elif time_option == 'month':
            pattern = '%Y-%m'
        elif time_option == 'year':
            pattern = '%Y'
        df_agg[time_option] = df_agg[time_option].apply(lambda x: x.strftime(pattern))

        #avg pace all activities
        df_agg['avg_pace'] = df_agg['time']*60/df_agg['distance']

        #running avg pace
        df_agg_notX = filt_df[~filt_df.type.isin([blockNames.RunTypes.X, blockNames.RunTypes.XB])][needed_cols].resample(agg_option, on='date').sum()
        df_agg_notX['run_avg_pace'] = df_agg_notX['time']*60/df_agg_notX['distance']

        df_agg = pd.concat([df_agg, df_agg_notX['run_avg_pace']], axis=1)

        df_agg['%E'] = 100*df_agg['distE'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])
        df_agg['%M'] = 100*df_agg['distM'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])
        df_agg['%T'] = 100*df_agg['distT'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])
        df_agg['%I'] = 100*df_agg['distI'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])
        df_agg['%R'] = 100*df_agg['distR'] / (df_agg['distE'] + df_agg['distI'] + df_agg['distM'] + df_agg['distR'] + df_agg['distT'])

        cols = ['%E','%M','%T','%I','%R']
        df_agg['%types'] = df_agg[cols].apply(lambda row: "%.0f(%.0f)%%/%.0f%%/%.0f%%/%.0f%%"%(row.values[0]+row.values[1],row.values[1],row.values[2],row.values[3],row.values[4]), axis=1)

        decimals = pd.Series([1, 1, 0, 0, 1, 1, 1, 1, 1], index=['distance', 'time', 'climb', 'run_avg_pace', '%E', '%M', '%T', '%I', '%R'])

        return df_agg.round(decimals).to_json(date_format='iso', orient='split')

    @app.callback(
        dash.dependencies.Output('weekly_agg', 'children'),
        [dash.dependencies.Input('type-dropdown', 'value')]
    )
    def weekly_summary(chosen_basic_runTypes):
        return time_aggregate(chosen_basic_runTypes, 'week')

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
                {"name": "Run Avg.Pace", "id": "run_avg_pace"},
                {"name": "E(M)%/T%/I%/R%", "id": "%types"},
            ]
        return columns

    @app.callback(
        dash.dependencies.Output('monthly_agg', 'children'),
        [dash.dependencies.Input('type-dropdown', 'value')]
    )
    def weekly_summary(chosen_basic_runTypes):
        return time_aggregate(chosen_basic_runTypes, 'month')

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
                {"name": "Run.Avg.Pace", "id": "run_avg_pace"},
            ]
        return columns

    @app.callback(
        dash.dependencies.Output('yearly_agg', 'children'),
        [dash.dependencies.Input('type-dropdown', 'value')]
    )
    def weekly_summary(chosen_basic_runTypes):
        return time_aggregate(chosen_basic_runTypes,'year')

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
                {"name": "Run.Avg.Pace", "id": "run_avg_pace"},
            ]
        return columns

    @app.callback(
        dash.dependencies.Output('agg_graph', 'figure'),
        [dash.dependencies.Input('xaxis-column2', 'value'),
         dash.dependencies.Input('yaxis-column2', 'value'),
         dash.dependencies.Input('type-dropdown', 'value'),
         dash.dependencies.Input('agg_df', 'children')])
    def update_figure(xaxis_colname, yaxis_colname, chosen_basic_runTypes, df_agg_json):
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
                chosen_basic_runTypes = [
                                         blockNames.RunTypes.E, 
                                         blockNames.RunTypes.M,
                                         blockNames.RunTypes.T,
                                         blockNames.RunTypes.I,
                                         blockNames.RunTypes.R
                                        ]

            traces = [
                go.Bar(
                    x=df_agg[:][xaxis_colname],
                    y=df_agg[:][str_template%i],
                    opacity=0.5,
                    hovertext = df_agg[:][yaxis_colname],
                    marker={ 'color': runTypesToColors[i] },
                    name=i
                ) for i in basic_runType_order if i in chosen_basic_runTypes
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
                height=300,
                width=600,
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
        dash.dependencies.Output('freq_graph', 'figure'),
        [dash.dependencies.Input('type-dropdown', 'value'),
        dash.dependencies.Input('year-slider', 'value')]
    )
    def update_figure(chosen_basic_runTypes, chosen_year):
        #Apply filters
        if chosen_year == df.date.dt.year.max()+2:
            filt_df = df
        elif chosen_year == df.date.dt.year.max()+1:
            today = datetime.datetime.now()
            last_year = subtract_weeks(today, weeks=52)
            filt_df = df[np.logical_and(df.date >= last_year, df.date <= today)]
        else:
            filt_df = df[df.date.dt.year == chosen_year]

        filt_df = filt_df[filt_df.type.isin(chosen_basic_runTypes)]

        counts = get_running_location_count(filt_df)
        counts = counts.loc[counts.counts >1]

        traces = [
            go.Bar(
                y=counts.index,
                x=counts.counts,
                opacity=0.5,
                marker={ 'color': '#1f77b4' },
                name='All',
                orientation='h'
            ) 
        ]

        return {
            'data': traces,
            'layout': go.Layout(
                height=300,
                width=600,
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
        columns = ['avg_dist', 'sd_dist', 'avg_time', 'sd_time', 'avg_climb', 'sd_climb']
        summary_df = pd.DataFrame(index=index, columns=columns)

        aggs = [w_agg.iloc[-5:-1], w_agg[:-1], m_agg.iloc[:-1], y_agg]
        variables = ['distance', 'time', 'climb']
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
            ]
        return columns


    return app

if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
