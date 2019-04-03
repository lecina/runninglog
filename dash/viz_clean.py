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

def read_pandas_pickle(fname = "../../running_log_data/processed/df.pkl"):
    df = pd.read_pickle(fname)
    df.date = pd.to_datetime(df.date)
    return df

def get_year_marks(df):
    years = df.date.dt.year
    year_marks={year: str(year) for year in np.hstack([years.unique(), [years.max()+1]])}
    year_marks[years.max()+1] = 'All'

    return year_marks

def get_runType_order():
    runType_order = [blockNames.RunTypes.E, 
                     blockNames.RunTypes.M,
                     blockNames.RunTypes.T,
                     blockNames.RunTypes.I,
                     blockNames.RunTypes.R,
                     blockNames.RunTypes.C,
                     blockNames.RunTypes.X]
    return runType_order

def get_basic_runTypes_order():
    runType_order = [blockNames.RunTypes.E, 
                     blockNames.RunTypes.M,
                     blockNames.RunTypes.T,
                     blockNames.RunTypes.I,
                     blockNames.RunTypes.R,
                     blockNames.RunTypes.X]
    return runType_order

def get_runType_colors(runType_order):
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

    return runTypesToColors

def get_ordered_runType_long_name(runType_order):
    return [{'value':rt, 'label':blockNames.RUN_TYPES_LONG_NAME_DICTIONARY[rt] } for rt in runType_order]

def get_available_columns():
    available_cols = ['distance', 'time', 'climb', 'avg_pace']
    #available_cols.append('week')
    return available_cols

def get_time_options():
    time_agg_options = ['day', 'week', 'month', 'year']
    return time_agg_options

def main():
    basic_runType_order = get_basic_runTypes_order() #E,M,T,I,R,X

    runType_order = get_runType_order() #E,M,T,I,R,X,C
    runTypesToColors = get_runType_colors(runType_order)
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
                    value=max(year_marks.keys()),
                    step=1,
                    marks=year_marks,
                    included=False
                )
            ], style={'width': '35%', 'display': 'inline-block', 'padding': '0px 0px 0px 20px'}),
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
                            'padding': '0px 0px 5px 0px'
                        })
        ]),
        html.Div([
            dcc.Dropdown(
                id='type-dropdown',
                options=runTypes_long_name,
                value=[blockNames.RunTypes.X, blockNames.RunTypes.C, blockNames.RunTypes.R, blockNames.RunTypes.I, blockNames.RunTypes.T, blockNames.RunTypes.M, blockNames.RunTypes.E],
                multi = True
            )], style={'padding':'10px 10px 10px 10px'}),
        html.Div(id='agg_df', style={'display': 'none'}), #hidden, in order to share data
        html.Div(id='weekly_agg', style={'display': 'none'}), #hidden, in order to share data
        html.Div(id='monthly_agg', style={'display': 'none'}), #hidden, in order to share data
        html.Div(id='yearly_agg', style={'display': 'none'}), #hidden, in order to share data
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='yaxis-column2',
                    options=[{'label': i, 'value': i} for i in available_cols],
                    value='distance'
                ),
            ], style={'width':'49%', 'display': 'inline-block', 'height':'30px'}),
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column2',
                    options=[{'label': i, 'value': i} for i in time_agg_options],
                    value='week'
                ),
            ],style={'width':'49%', 'display': 'inline-block', 'height':'30px'}),
            dcc.Graph(id='agg_graph') #graph!
        ],style={'display':'inline-block', 'width':'49%', 'float':'left', 'height':'430px'}),
        #display:flex;justify-content:center;align-items:center

        html.Div([
            html.Div([html.H5("Weekly summary:"),],style={'height':'30px', 'textAlign':'center'}),
            dash_table.DataTable(
                    id='weekly_agg_table',
                    data=df.to_dict('rows'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    #columns=[
                    #        {"name": ["", "Date"], "id": "date"},
                    #        {"name": ["", "Type"], "id": "type"},
                    #        {"name": ["", "Dist."], "id": "distance"},
                    #        {"name": ["", "Climb"], "id": "climb"},
                    #        {"name": ["", "Time"], "id": "time"},
                    #        {"name": ["", "Where"], "id": "where"},
                    #        {"name": ["", "Notes"], "id": "notes"},
                    #        {"name": ["", "Avg. Pace"], "id": "avg_pace"},
                    #    ],
                    style_table={
                        'overflowX': 'scroll', 
                        'maxHeight': '400',
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
                    #n_fixed_columns=1,
                    n_fixed_rows=1,
                    style_as_list_view=True,
                    merge_duplicate_headers=True,
                    style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold'
                        },
                    sorting=True,
                    sorting_type="multi",
                ),
        ], style={'width':'49%', 'display':'inline-block','justify-content':'center','align-items':'center', 'height':'430px'}),

        html.Div([
            html.Div([html.H5("Monthly summary:"),],style={'height':'30px', 'textAlign':'center'}),
            dash_table.DataTable(
                    id='monthly_agg_table',
                    data=df.to_dict('rows'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    style_table={
                        'overflowX': 'scroll', 
                        'maxHeight': '360',
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
                    #n_fixed_columns=1,
                    n_fixed_rows=1,
                    style_as_list_view=True,
                    merge_duplicate_headers=True,
                    style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold'
                        },
                    sorting=True,
                    sorting_type="multi",
                ),
        ], style={'width':'49%', 'display':'inline-block','justify-content':'center','align-items':'center', 'float':'left', 'padding-top':'10px'}),
        html.Div([
            html.Div([html.H5("Yearly summary:"),],style={'height':'30px', 'textAlign':'center'}),
            dash_table.DataTable(
                    id='yearly_agg_table',
                    data=df.to_dict('rows'),
                    columns=[{'id': c, 'name': c} for c in df.columns],
                    style_table={
                        'overflowX': 'scroll', 
                        'maxHeight': '360',
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
                    #n_fixed_columns=1,
                    n_fixed_rows=1,
                    style_as_list_view=True,
                    merge_duplicate_headers=True,
                    style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold'
                        },
                    sorting=True,
                    sorting_type="multi",
                ),
        ], style={'width':'49%', 'display':'inline-block','justify-content':'center','align-items':'center', 'padding-top':'10px'})
    ])

    @app.callback(
        dash.dependencies.Output('agg_df', 'children'),
        [dash.dependencies.Input('xaxis-column2', 'value'),
        dash.dependencies.Input('yaxis-column2', 'value'),
        dash.dependencies.Input('type-dropdown', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        dash.dependencies.Input('date-picker-range', 'start_date'),
        dash.dependencies.Input('date-picker-range', 'end_date')])
    def agg_data(xaxis_colname, yaxis_colname, 
                        chosen_basic_runTypes, chosen_year,
                        start_date, end_date):
        #Apply filters
        if chosen_year == df.date.dt.year.max()+1:
            filt_df = df
        else:
            filt_df = df[df.date.dt.year == chosen_year]

        filt_df = filt_df[filt_df.type.isin(chosen_basic_runTypes)]

        filt_df = filt_df[np.logical_and(filt_df.date >= start_date, filt_df.date <= end_date)]
        #END apply filters

        if xaxis_colname == 'day':
            xaxis_colname = 'date'

        #if ycol is distance, segment it by types
        if yaxis_colname == 'distance':
            distance_cols = 'dist%s'
            needed_cols = [distance_cols%bt for bt in basic_runType_order]
            needed_cols.extend(['distance', 'date'])
        else:
            needed_cols = [yaxis_colname, 'date']

        if xaxis_colname == 'week':
            agg_str = 'W'
        elif xaxis_colname == 'month':
            agg_str = 'MS'
        elif xaxis_colname == 'year':
            agg_str = 'YS'
        else:
            agg_str = None

        if not agg_str is None:
            df_agg = filt_df[:][needed_cols].resample(agg_str, on='date').sum()
            df_agg[xaxis_colname] = df_agg.index
        else:
            df_agg = filt_df

        return df_agg.to_json(date_format='iso', orient='split')


    def time_aggregate(chosen_basic_runTypes, chosen_year, start_date, end_date, time_option):
        if time_option == 'week':
            agg_option = 'W'
        elif time_option == 'month':
            agg_option = 'MS'
        elif time_option == 'year':
            agg_option = 'YS'
        else:
            agg_option = 'W'

        #Apply filters
        if chosen_year == df.date.dt.year.max()+1:
            filt_df = df
        else:
            filt_df = df[df.date.dt.year == chosen_year]

        filt_df = filt_df[filt_df.type.isin(chosen_basic_runTypes)]

        filt_df = filt_df[np.logical_and(filt_df.date >= start_date, filt_df.date <= end_date)]
        #END apply filters

        #if ycol is distance, segment it by types
        distance_cols = 'dist%s'

        needed_cols = ['date', 'distance', 'time', 'climb']
        df_agg = filt_df[:][needed_cols].resample(agg_option, on='date').sum()
        df_agg[time_option] = df_agg.index
        if time_option == 'week':
            pattern = '%Y-%m-%d'
        elif time_option == 'month':
            pattern = '%Y-%m'
        elif time_option == 'year':
            pattern = '%Y'
        df_agg[time_option] = df_agg[time_option].apply(lambda x: x.strftime(pattern))

        df_agg_notX = filt_df[filt_df.type != blockNames.RunTypes.X][needed_cols].resample(agg_option, on='date').sum()
        df_agg_notX['run_avg_pace'] = df_agg_notX['time']*60/df_agg_notX['distance']

        df_agg = pd.concat([df_agg, df_agg_notX['run_avg_pace']], axis=1)

        decimals = pd.Series([1, 1, 0, 0], index=['distance', 'time', 'climb', 'run_avg_pace'])

        return df_agg.round(decimals).to_json(date_format='iso', orient='split')

    @app.callback(
        dash.dependencies.Output('weekly_agg', 'children'),
        [dash.dependencies.Input('type-dropdown', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        dash.dependencies.Input('date-picker-range', 'start_date'),
        dash.dependencies.Input('date-picker-range', 'end_date')])
    def weekly_summary(chosen_basic_runTypes, chosen_year, start_date, end_date):
        return time_aggregate(chosen_basic_runTypes, chosen_year, start_date, end_date,'week')

    @app.callback(
        dash.dependencies.Output('weekly_agg_table', 'data'),
        [dash.dependencies.Input('weekly_agg', 'children')])
    def update_figure(df_agg_json):
        df_agg = pd.read_json(df_agg_json, orient='split')

        df_agg['time'] = df_agg['time'].apply(lambda x: '{:d}h {:0>2d}m'.format(int(x//60), int(x%60)))
        df_agg['run_avg_pace'] = df_agg['run_avg_pace'].apply(lambda x: "{:d}:{:0>2d}".format(int(x//60),int(x%60)))

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
                {"name": "Run.Avg.Pace", "id": "run_avg_pace"},
            ]
        return columns

    @app.callback(
        dash.dependencies.Output('monthly_agg', 'children'),
        [dash.dependencies.Input('type-dropdown', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        dash.dependencies.Input('date-picker-range', 'start_date'),
        dash.dependencies.Input('date-picker-range', 'end_date')])
    def weekly_summary(chosen_basic_runTypes, chosen_year, start_date, end_date):
        return time_aggregate(chosen_basic_runTypes, chosen_year, start_date, end_date,'month')

    @app.callback(
        dash.dependencies.Output('monthly_agg_table', 'data'),
        [dash.dependencies.Input('monthly_agg', 'children')])
    def update_figure(df_agg_json):
        df_agg = pd.read_json(df_agg_json, orient='split')

        df_agg['time'] = df_agg['time'].apply(lambda x: '{:d}h {:0>2d}m'.format(int(x//60), int(x%60)))
        df_agg['run_avg_pace'] = df_agg['run_avg_pace'].apply(lambda x: "{:d}:{:0>2d}".format(int(x//60),int(x%60)))

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
        [dash.dependencies.Input('type-dropdown', 'value'),
        dash.dependencies.Input('year-slider', 'value'),
        dash.dependencies.Input('date-picker-range', 'start_date'),
        dash.dependencies.Input('date-picker-range', 'end_date')])
    def weekly_summary(chosen_basic_runTypes, chosen_year, start_date, end_date):
        agg_df = time_aggregate(chosen_basic_runTypes, chosen_year, start_date, end_date,'year')
        return agg_df

    @app.callback(
        dash.dependencies.Output('yearly_agg_table', 'data'),
        [dash.dependencies.Input('yearly_agg', 'children')])
    def update_figure(df_agg_json):
        df_agg = pd.read_json(df_agg_json, orient='split')

        df_agg['time'] = df_agg['time'].apply(lambda x: '{:d}h {:0>2d}m'.format(int(x//60), int(x%60)))
        df_agg['run_avg_pace'] = df_agg['run_avg_pace'].apply(lambda x: "{:d}:{:0>2d}".format(int(x//60),int(x%60)))

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

        if yaxis_colname == 'distance':
            distance_template = 'dist%s'
            traces = [
                go.Bar(
                    x=df_agg[:][xaxis_colname],
                    y=df_agg[:][distance_template%i],
                    opacity=0.5,
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
                height=400,
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




    return app

if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
