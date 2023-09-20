import dash
from dash import html, callback, Input, Output

# from DashApp2023.apps import survey_unit_dropdown
from DashApp2023.apps import scatter_plot
from DashApp2023.apps import error_bar_plot

# from DashApp2023.apps import leaflet_map
from DashApp2023.apps import mapbox

from DashApp2023.apps import profile_line_plot
from DashApp2023.apps import CSA_Table
import dash_bootstrap_components as dbc
from dash import dcc
import psycopg2
import geopandas as gpd
import json
from dash_extensions.javascript import Namespace

# register the page with dash giving url path
dash.register_page(__name__, path="/main_dash2")
layout = html.Div([
    dbc.Row(
            [
                dbc.Col(html.Div([
                    mapbox.layout,

                ],
                    style={'margin-left': '20px'}),

                    width={"size": 6, "offset":0},),

                dbc.Col(html.Div(
                    scatter_plot.layout,

                ),  style={'margin-top': '20px'},
                    width={"size": 6, "offset":0}),
            ],
            align="start"

        ),
    dbc.Row(
        [
            dbc.Col(html.Div(profile_line_plot.layout),width={"size": 6, "offset":0}),
            dbc.Col(html.Div(error_bar_plot.layout),width={"size": 6, "offset":0}),

        ],
        align="center",),













    ])
