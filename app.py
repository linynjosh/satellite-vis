# -*- coding: utf-8 -*-
# Import required libraries
import pandas as pd
import numpy as np
import dash
import pathlib
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


# TODO: ---------------- Read in data
df = 

# TODO: Get our list of countries
countries = 

# Get our labels for the dropdown menus
country_labels = []
for country in countries:
    country_labels.append({'label': country, 'value': country})

# TODO: Get our list of launch years
years = 

# TODO: Get our list of purposes
purposes = 

# Get our purpose labels for the dropdown menus
purpose_labels = []
for purpose in purposes:
    purpose_labels.append({'label': purpose, 'value': purpose})


# ------------------------------ Setup the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

TEXTS = {
    0: """
    ##### Satellites per country over the years
    Write something
    """,
    1: """
    ##### Satellite Purposes per Purpose
    Write something
    """
}


# ------------------ set layout of the graph
app.layout = html.Div(
    [
        dcc.Store(id="click-output"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url("satellite.png"),
                                    className="plotly-logo",
                                )
                            ]
                        ),
                        dcc.Markdown(
                            """
                            ### Josh gives a title
                            """,
                            className="title",
                        ),
                        dcc.Markdown(
                            """This interactive report is... """,
                            className="subtitle",
                        ),
                    ]
                ),
            ],
            className="four columns sidebar",
        ),
        html.Div(
            [
                html.Div([dcc.Markdown(TEXTS[0])], className="text-box"),
                dcc.Dropdown(
                    id="dropdown1",
                    options=country_labels,
                    value=['USA'],
                    multi=True
                ),
                dcc.Graph(id="graph1", style={"margin": "0px 20px", "height": "45vh"}),
                html.Div([dcc.Markdown(TEXTS[0])], className="text-box"),
                dcc.Dropdown(
                    id="dropdown2",
                    options=purpose_labels,
                    value=['Commercial'],
                    multi=True
                ),
                dcc.Graph(id="graph2", style={"margin": "0px 20px", "height": "45vh"}),
            ],
            id="page",
            className="eight columns",
        ),
    ],
    className="row flex-display",
    style={"height": "100vh"},
)

# ---------------------- helper functions
# TODO:
def sat_by_country_and_purpose(country, purpose):


# TODO:
def total_sat_by_country(country):



# ------------------------- plotting functions

# Make graphs
@app.callback(Output("graph1", "figure"), [Input("dropdown1", "value")])
def plot_total_sat_by_country(countries):

    # TODO: Create figure

    return fig

# Make graphs
@app.callback(Output("graph2", "figure"), 
[Input("dropdown1", "value"), Input("dropdown2", "value")])
def plot_sat_by_country_and_purpose(countries, purposes):

    # TODO: Create figure

    return fig

# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
