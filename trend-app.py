#!/c/Users/andrewkl/AppData/Local/Programs/Python/Python311/python
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

# Place holder graph before data is pulled
fig_empty = go.Figure()
fig_empty.add_trace(go.Scatter(x=[0], y=[0], name='NO DATA'))
fig_empty.add_annotation(x=0, y=0,text="ENTER FILE PATH",showarrow=False,yshift=10)

# Graph component
trend_plot = dcc.Graph(id="trend_plot", responsive=True, style={'height': '750px'})

# App Layout
app.layout = dbc.Container([
    html.H1("Trend Analysis", style={'margin': 10}),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Label('Enter full path to data file: ', style={'margin': 10}),
            dcc.Input(id='full_path', type='text', placeholder='File Path...', style={'margin': 10,'width': '650px'})
        ])
    ]),
    dbc.Row([
        dbc.Col([
            trend_plot
            ])
        ])
    ], fluid=True)

# Update plot with data
@app.callback(
    Output('trend_plot','figure'),
    Input('full_path','value')
)
def update_plot(value):
    if value != None:
        full_path = value
        split_path = full_path.rsplit('\\', 1)
        # Pull data store as df
        folder_path = split_path[0]
        file_name = split_path[1]

        df = pd.read_csv(full_path, header=0, index_col=False, parse_dates=[0])

        # Trend plot
        fig = go.Figure()
        for column in df.columns:
            if column != 'Time':
                fig.add_trace(go.Scatter(x=df['Time'], y=df[column], name=column))
        plot_title = file_name.split('.')[0] + ' Plot'
        fig.update_layout(title=plot_title,
                        xaxis_title="",
                        yaxis_title="",
                        legend_title="Trend Variables")
        return fig
    else:
        return fig_empty

if __name__ == "__main__":
    app.run_server(debug=True)  # host="0.0.0.0", port="8052")
