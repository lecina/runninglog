import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px
import base64

import umap
import pandas as pd
import numpy as np

from runninglog.utilities import utilities
from runninglog.constants import blockNames
from runninglog.run import types

try:
    from viz.viz_constants import viz_constants
except:
    from viz_constants import viz_constants



def create_scatter(df, cols, colors=None, colortitle=None, symbols=None, scale=True):
        #return px.scatter(df, x='umap_X1', y='umap_X2', color='type', symbol='trail')#, text=[df.loc[i,cols].to_string().replace("\n", "<br>") for i in range(len(df.index))])
        runTypesToColors = viz_constants.get_runType_colors()
        if colors is None:
            colors = [runTypesToColors[x] for x in df.type]
        if symbols is None:
            symbols = ['circle' if x==0 else 'diamond' for x in df.trail]

        scatter = go.Scatter(
            x=df.loc[:, 'umap_X1'],
            y=df.loc[:, 'umap_X2'],
            text=[df.loc[i,cols].to_string().replace("\n", "<br>") for i in range(len(df.index))],
            mode='markers',
            showlegend = True,
            marker={
                'size': 10,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': ['white' if x==0 else 'black' for x in df.trail]},
                'symbol' : symbols, 
                'color' : colors,
                #'colorscale': runTypesToColors.values(),
                'colorbar' : { 'title':colortitle},
                'showscale' : scale
            }
        )
        return scatter

def update_umap_figure(df, cols, title=None, colors=None, symbols=None):
    #return create_scatter(df,cols, colors=colors, symbols=symbols, scale=False)
    runTypesToColors = viz_constants.get_runType_colors()
    figure= {
        'data': [create_scatter(df,cols, colors=colors, symbols=symbols, scale=False)],
        'layout': go.Layout(
            xaxis={ 'title': 'X1'},
            yaxis={ 'title': 'X2'},
            title=title,
            height=400,
            margin={'l': 30, 'b': 30, 't': 30, 'r': 30},
            showlegend = False,
            hovermode='closest'
        )
    }
    return figure

def update_umap_explain_figure(df, cols, title, logColors=False):
    runTypesToColors = viz_constants.get_runType_colors()
    if logColors == True:
        colors = np.log10(df[title]+min(df[title])+10) - 1
    else:
        colors = df[title]
    figure= {
        'data': [create_scatter(df,cols, colors=colors)],
        'layout': go.Layout(
            xaxis={ 'title': 'X1'},
            yaxis={ 'title': 'X2'},
            title=title,
            height=200,
            margin={'l': 30, 'b': 30, 't': 30, 'r': 30},
            showlegend = False,
            hovermode='closest'
        )
    }
    return figure

def update_distr_plot_figure(df, col, title=None, agg_all=False):
    if not agg_all:
        runTypesToColors = viz_constants.get_runType_colors()
        groups = types.RUNNING_ACTIVITIES
        colors = [runTypesToColors[type] for type in groups]
        x = [df[df.type == type][col] for type in groups]
    else:
        df_notX = df[df.type.isin(types.RUNNING_ACTIVITIES)]

        years = set(df_notX.date.dt.year)

        x = [df_notX[col]]
        x.extend([df_notX[df_notX.date.dt.year == year][col] for year in years])

        groups = ['All']
        groups.extend([str(year) for year in years])

        colors = px.colors.sequential.Burg

    #TODO rug_text
    fig = ff.create_distplot(x, groups, show_hist=False, colors=colors, curve_type='kde')

    if agg_all:
        fig.update_traces(line=dict(width=5, dash='dash', color='#4682b4'),selector=dict(mode='lines', legendgroup='All'))

    layout = go.Layout(
        xaxis={ 'title': col},
        yaxis={ 'title': 'Density'},
        title=title,
        height=400,
        margin={'l': 30, 'b': 30, 't': 30, 'r': 30},
        hovermode='closest',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
        )
    fig.update_layout(layout)
    return fig

def main():
    app = dash.Dash(__name__)

    df = utilities.read_pandas_pickle("data/processed/df.pkl")

    available_cols = list(df.columns)

    cols = ['climb', u'distance', 'time', 'date', 'type', 'where', u'distE', u'distI', u'distM', u'distR', u'distT', u'distX', u'distXB', 'trail']

    encoded_image = base64.b64encode(open('img/logo.png', 'rb').read()).decode('ascii')


    app.layout = html.Div([
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(encoded_image), style={'height':'40px', 'display':'inline-block', 'margin':'5px 0px 0px 10px'}),
           html.H2("Running log - Exploration", style={'display':'inline-block', 'vertical-align': 'center', 'margin':'0px', 'padding':'3px 0px 5px 20px'}) 
        ], style={'background-color':'#6BC06D', 'height':'50px', 'vertical-align': 'center', 'padding':'0px', 'margin':'0px', 'margin-block-start':'0px', 'display':'flex'}),
        html.Div([
            html.H3("UMAP projection"),
            html.Div([
                dcc.Graph(id='umap_graph', figure=update_umap_figure(df, cols, title='Runs - UMAP projection'))
            ], style={'width':'60%', 'display':'inline-block', 'float':'left'}),
            html.Div([
                dcc.Graph(id='umap_graph_dist', figure=update_umap_explain_figure(df, cols, 'distance')),
                dcc.Graph(id='umap_graph_climb', figure=update_umap_explain_figure(df, cols, 'climb', logColors=True))
            ], style={'width':'20%', 'display':'inline-block'}),
            html.Div([
                dcc.Graph(id='umap_graph_time', figure=update_umap_explain_figure(df, cols, 'time', logColors=True)),
                dcc.Graph(id='umap_graph_pace', figure=update_umap_explain_figure(df, cols, 'avg_pace', logColors=True))
            ], style={'width':'20%', 'display':'inline-block'})
        ], style={'width':'100%', 'display':'block', 'margin':'auto'}),
        html.Div([
            html.H3("Variable relation"),
            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_cols],
                    value='distance'
                ),
                dcc.RadioItems(
                    id='yaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '50%', 'display': 'inline-block', 'float':'left'}),

            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_cols],
                    value='time'
                ),
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='graph_scatter')
        ], style={'width':'80%', 'display':'block', 'float':'center', 'margin':'auto'}),
        html.Div([
            html.Div([
                dcc.Graph(id='graph_distr_dist', figure=update_distr_plot_figure(df,'distance', 'Dist. density', agg_all=True))
            ], style={'width':'33%', 'display':'inline-block', 'float':'left', 'margin':'auto'}),
            html.Div([
                dcc.Graph(id='graph_distr_time', figure=update_distr_plot_figure(df,'time', 'Time density', agg_all=True))
            ], style={'width':'33%', 'display':'inline-block', 'margin':'auto'}),
            html.Div([
                dcc.Graph(id='graph_distr_climb', figure=update_distr_plot_figure(df,'climb', 'Climb density', agg_all=True))
            ], style={'width':'33%', 'display':'inline-block', 'margin':'auto'}),
            html.Div([
                dcc.Graph(id='graph_distr_dist_types', figure=update_distr_plot_figure(df,'distance', 'Dist. density by type', agg_all=False))
            ], style={'width':'50%', 'display':'inline-block', 'float':'left', 'margin':'auto'}),
            html.Div([
                dcc.Graph(id='graph_distr_time_types', figure=update_distr_plot_figure(df,'time', 'Time. density by type', agg_all=False))
            ], style={'width':'50%', 'display':'inline-block', 'margin':'auto'}),
        ], style={'width':'100%', 'display':'block', 'float':'center', 'margin':'auto'}),
    ])


    @app.callback(
        dash.dependencies.Output('graph_scatter', 'figure'),
        [dash.dependencies.Input('xaxis-column', 'value'),
         dash.dependencies.Input('yaxis-column', 'value'),
         dash.dependencies.Input('xaxis-type', 'value'),
         dash.dependencies.Input('yaxis-type', 'value')])
    def update_figure(xaxis_column_name, yaxis_column_name,
                     xaxis_type, yaxis_type):
        traces = [
                    go.Scatter(
                        x=df[df['type'] == i][xaxis_column_name],
                        y=df[df['type'] == i][yaxis_column_name],
                        mode='markers',
                        text=[df.loc[j, cols].to_string().replace("\n", "<br>") for j in df[df.type==i].index],
                        opacity=0.5,
                        marker={
                            'size': 15,
                            'symbol': ['circle' if x==0 else 'diamond' for x in df[df.type==i].trail],
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in ['E', 'M', 'T', 'I', 'R', 'X', 'XB']
        ]

        return {
            'data': traces,
            'layout': go.Layout(
                xaxis={'title': xaxis_column_name, 'type': 'linear' if xaxis_type == 'Linear' else 'log'},
                yaxis={'title': yaxis_column_name, 'type': 'linear' if yaxis_type == 'Linear' else 'log'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }


    #return main app
    return app

if __name__ == '__main__':
    app = main()
    app.run_server(debug=True)
