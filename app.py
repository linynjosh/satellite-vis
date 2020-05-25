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
import plotly.express as px


# ---------------- Read in data
filename = "data/UCS-Satellite-Database-Officialname-4-1-2020.txt"
data = pd.read_csv(filename, sep='\t', error_bad_lines=False)
df = data.iloc[0:2666,[i for i in range(30)]]

# Get our list of countries
countries = []
for item in df['Country of Operator/Owner'].tolist():
    countries += item.split("/")
countries = list(set(countries))

# Get our labels for the dropdown menus
country_labels = []
for country in countries:
    country_labels.append({'label': country, 'value': country})

# Get our list of launch years
years = []
for item in df['Date of Launch'].tolist():
    years.append(item.split("/")[2])
years = list((set(years)))
years.sort()

# Get our list of purposes
purposes = []
for purpose in df['Users'].unique():
    if ' ' not in purpose and '/' not in purpose:
        purposes.append(purpose)

# Get our purpose labels for the dropdown menus
purpose_labels = []
for purpose in purposes:
    purpose_labels.append({'label': purpose, 'value': purpose})


# ------------------------------ Setup the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.title = 'Satellites'
server = app.server

TEXTS = {
    0: """
    ##### Satellites Per Country Over the Years
    There are currently around 2666 satellites orbiting the earth in 2020. These satellites have different countries of origin and are designed for distinct purposes. As of today, America has the most satellites, while China and Russia have the second and third most satellites. 
    
    """,
    1: """
    ##### The Purposes of Satellites for Each Country Over the Years
    Satellites are mainly operated for commercial, military, government, and civil purposes as seen in the following graph. 

    """
}
COLOR = px.colors.qualitative.Alphabet
MARKER = ['diamond-tall', 'circle', 'triangle-up', 'square']


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
                            ### Satellites
                            """,
                            className="title",
                        ),
                        dcc.Markdown(
                            "This interactive report shows the number of satellites launched and operated by a country at any specific year spanning from 1975-2020. In addition, the purposes of the satellites are shown in every country in the same period.",
                            className="subtitle",)
                    ]
                ),
            ],
            className="three columns sidebar",
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
                dcc.Graph(id="graph1", style={"margin": "0px 20px", "height": "80vh"}),
                html.Div([dcc.Markdown(TEXTS[1])], className="text-box"),
                dcc.Dropdown(
                    id="dropdown2",
                    options=purpose_labels,
                    value=['Commercial'],
                    multi=True
                ),
                dcc.Graph(id="graph2", style={"margin": "0px 20px", "height": "80vh"}),
            ],
            id="page",
            className="eight columns",
        ),
    ],
    className="row flex-display",
    style={"height": "220vh"},
)

# ---------------------- helper functions

def sat_by_country_and_purpose(country, purpose):
    """
       This function finds the purpose of the satellites launched by a country at a specific year.

       Inputs:
           country - a string
           purpose - a string
       Returns:
           results - dict key (years - string) and value (integer)

       """
    results = {}
    for items in years:
        sub = df[
            (df['Country of Operator/Owner'].str.contains(country)) &
            (df['Users'].str.contains(purpose)) &
            (df['Date of Launch'].str.contains(items))
            ]
        results[items] = sub.shape[0]
    return results

def total_sat_by_country(country):
    """
    This function calculates the total satellites launched by a country at a specific year

    Inputs:
        country - a string
    Returns:
        results - dict key (years - string) and value (integer)

    """
    results = {}
    for items in years:
        sub = df[
            (df['Country of Operator/Owner'].str.contains(country)) &
            (df['Date of Launch'].str.contains(items))
            ]
        results[items] = sub.shape[0]
    return results


# ------------------------- plotting functions
# Make graphs
@app.callback(Output("graph1", "figure"), [Input("dropdown1", "value")])
def plot_sat_by_country(value):
    # Create figure
    fig = go.Figure()
    for i, count in enumerate(value):
        results = total_sat_by_country(count)
        fig.add_trace(go.Scatter(
            x=list(results.keys()),
            y=list(results.values()),
            name=count,
            fill='tozeroy',
            line=dict(
                color=COLOR[i]
            )
        ))
    # Add range slider
    fig.update_layout(
        title_text="Number of Launched Per Year",
        showlegend=True,
        xaxis=dict(
            rangeslider=dict(
                visible=True
            )
        ),
    )
    return fig
# Make graphs
@app.callback(Output("graph2", "figure"),
[Input("dropdown1", "value"), Input("dropdown2", "value")])
def plot_sat_by_country_and_purpose(countries, purposes):
    # Create figure
    fig = go.Figure()
    for i, country in enumerate(countries):
        for j, purpose in enumerate(purposes):
            results = sat_by_country_and_purpose(country, purpose)
            fig.add_trace(go.Scatter(
                x=list(results.keys()),
                y=list(results.values()),
                name=country+": "+purpose,
                mode='lines+markers',
                marker_symbol=MARKER[j]+"-open-dot",
                marker_size=8,
                line=dict(
                    color=COLOR[i],
                    width=0.5,
                    dash='dot'
                )
            ))
    # Add range slider, title, legend
    fig.update_layout(
        title_text="Number of Satellites Launched Per Year by Category",
        showlegend=True,
        plot_bgcolor = 'rgb(250,250,250)',
        xaxis=dict(
            rangeslider=dict(
                visible=True
            )
        )
    )
    return fig

# Run the Dash app
if __name__ == "__main__":
    app.run_server()
