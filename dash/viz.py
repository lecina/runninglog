import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_pickle("../../running_log_data/processed/df.pkl")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_cols = list(df.columns)

app.layout = html.Div([
    html.Div([

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
        ],
        style={'width': '48%', 'display': 'inline-block'}),

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
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    html.Label('Multi-Select Dropdown'),
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
    ),
    dcc.Graph(id='graph-with-dropdown')
])


@app.callback(
    dash.dependencies.Output('graph-with-dropdown', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('type-dropdown', 'value')])
def update_figure(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 selected_types):
    traces = [
                go.Scatter(
                    x=df[df['type'] == i][xaxis_column_name],
                    y=df[df['type'] == i][yaxis_column_name],
                    text=df[df['type'] == i]['date'],
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
            xaxis={'title': xaxis_column_name, 'type': 'linear' if xaxis_type == 'Linear' else 'log'},
            yaxis={'title': yaxis_column_name, 'type': 'linear' if yaxis_type == 'Linear' else 'log'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
