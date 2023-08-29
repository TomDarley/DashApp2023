import dash_bootstrap_components as dbc
from dash import html, dcc,callback, Input, Output
import numpy as np
import pandas as pd
import psycopg2
import geopandas as gpd
from scipy.interpolate import interp1d
from datetime import datetime
import matplotlib.dates as mdates
import plotly.express as px
import statsmodels.api as sm
import plotly.graph_objs as go
import sqlalchemy
from scipy.integrate import quad
import warnings
import time

layout = html.Div([
    dbc.Container(dbc.Row(
        [ dbc.Col(dcc.Graph(id="error_plot",
                              ),

                    width={"size": 12, 'offset': 0, "order": 2},
                    style={"margin-left": 0, "margin-top": 10, 'background-colour':'white' },

                    ),
        ]
    ),
    style={'background-color': '#1b1c1c',
           "margin": 0,       # Remove container margin
            "padding": 0 }      # Remove container padding

    )
])

@callback(
    (Output("error_plot", "figure")),
    [
        Input('survey-unit-dropdown', 'value'),
        Input('selected-df-storage', 'data')

    ],
)

def make_scatter_plot(selected_survey_unit, cpa_df):

    print(selected_survey_unit)
    df = pd.read_json(cpa_df)
    print(df)

    current_year = datetime.now().year
    survey_unit = selected_survey_unit

    # Create the scatter plot using Plotly Express
    fig = px.scatter( x=[1,2,3], y=[1,2,3],  height=600,
                     template='plotly_dark')


    return fig


















