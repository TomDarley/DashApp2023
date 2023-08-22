import dash_bootstrap_components as dbc
from dash import html, dcc,callback, Input, Output
import numpy as np
import pandas as pd
import psycopg2
import geopandas as gpd
from scipy.interpolate import interp1d

layout = html.Div([
    dbc.Container(dbc.Row(
        [
            dbc.Col(dcc.Graph(id="scatter_plot",
                              ),

                    width={"size": 6, 'offset': 0, "order": 2},
                    style={"margin-left": 0, "margin-top": 10},

                    )])

    )
])

#@callback(
#    (Output("scatter_plot", "figure")),
#    [
#        Input('selected-value-storage', 'data'),
#
#    ],
#)
