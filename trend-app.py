#!/c/Users/andrewkl/AppData/Local/Programs/Python/Python311/python
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objects as go

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY, dbc_css])

# Place holder graph before data is pulled
fig_empty = go.Figure()
fig_empty.add_trace(go.Scatter(x=[0], y=[0], name="NO DATA"))
fig_empty.add_annotation(
    x=0, y=0, text="ENTER FILE PATH OR SELECT DATA", showarrow=False, yshift=10
)

# Graph component
trend_plot = dcc.Graph(
    id="trend_plot", responsive=True, style={"height": "750px", "margin-top": 20}
)

# App Layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([html.H1("Trend Analysis", style={"margin": 6})], width=4),
                dbc.Col(
                    [
                        html.Label(
                            "Enter full path to data file:", style={"margin-top": 8}
                        ),
                        dbc.Input(
                            id="full_path",
                            type="text",
                            placeholder="File Path...",
                            style={
                                "margin-top": 8,
                                "margin-bottom": 8,
                                "width": "600px",
                            },
                            className="dbc",
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Load Data",
                            id="load-data-button",
                            n_clicks=0,
                            color="success",
                            size="lg",
                            className="me-1",
                        ),
                    ]
                ),
            ],
            align="center",
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Left y-axis", style={"margin": 3}),
                        dcc.Dropdown(
                            id="left-yaxis-columns",
                            multi=True,
                            className="dbc",
                            maxHeight=400,
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("Right y-axis", style={"margin": 3}),
                        dcc.Dropdown(
                            id="right-yaxis-columns",
                            multi=True,
                            className="dbc",
                            maxHeight=400,
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row([dbc.Col([trend_plot])]),
    ],
    fluid=True,
)

# Global variable to store the loaded data and file name
df = pd.DataFrame()
file_name = ""


# Update dropdown with data
@app.callback(
    [
        Output("left-yaxis-columns", "options"),
        Output("right-yaxis-columns", "options"),
        Output("right-yaxis-columns", "value"),
        Output("left-yaxis-columns", "value"),
    ],
    [Input("load-data-button", "n_clicks")],
    [State("full_path", "value")],
)
def update_dropdowns(n_clicks, file_path):
    global df
    global file_name

    if n_clicks > 0:
        # Read the CSV file
        df = pd.read_csv(file_path, header=0, index_col=False, parse_dates=[0])

        # Store file name golbally
        split_path = file_path.rsplit("\\", 1)
        file_name = split_path[1]

        # Generate options for dropdowns
        options = [{"label": col, "value": col} for col in df.iloc[:, 1:].columns]

        return options, options, [options[0]["value"]], []

    return [], [], [], []


# Update plot with data
@app.callback(
    Output("trend_plot", "figure"),
    [Input("left-yaxis-columns", "value"), Input("right-yaxis-columns", "value")],
)
def update_plot(left_axis, right_axis):
    global df

    if not left_axis and not right_axis:
        return fig_empty
    else:
        data = []

        # Create traces for right y-axis
        if right_axis is not None:
            for column in right_axis:
                trace = go.Scatter(
                    x=df["Time"],
                    y=df[column],
                    name=f"{column} (Right Y-axis)",
                    yaxis="y2",
                )
                data.append(trace)

        # Create traces for left y-axis
        if left_axis is not None:
            for column in left_axis:
                trace = go.Scatter(
                    x=df["Time"],
                    y=df[column],
                    name=f"{column} (Left Y-axis)",
                    yaxis="y",
                )
                data.append(trace)

        # Trend plot
        plot_title = file_name.split(".")[0] + " Plot"

        layout = go.Layout(
            title=plot_title,
            legend_title="Trend Variables",
            xaxis=dict(title="Time"),
            yaxis2=dict(overlaying="y", side="right"),
            showlegend=True,
        )

        fig = go.Figure(data=data, layout=layout)
        return fig


# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)  # host="0.0.0.0", port="8052")
