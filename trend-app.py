#!/usr/bin/env python3
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

# Pull data store as df
folder_path = r'C:\Users\andrewkl\McKinstry\MTN Projects - 12 Trends'
file = 'Scott-BIO-BAS-Combined.csv'
full_path = f'{folder_path}\\{file}'

df = pd.read_csv(full_path, header=0, index_col=False, parse_dates=[0])

# Trend plot
fig = go.Figure()
for column in df.columns:
    if column != 'Time':
        fig.add_trace(go.Scatter(x=df['Time'], y=df[column], name=column))
plot_title = file.split('.')[0] + ' Plot'
fig.update_layout(title=plot_title,
                xaxis_title="",
                yaxis_title="",
                legend_title="Trend Variables")

# Graph component
trend_plot = dcc.Graph(
            id="graph",
            figure=fig, responsive=True)

app.layout = dbc.Container([
    html.H1("Trend Analysis", style={'marginTop': 4, 'marginBottom': 2}),
    html.Hr(),
    dbc.Row([
        dbc.Col([trend_plot])
        ])
    ], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)  # host="0.0.0.0", port="8052")
