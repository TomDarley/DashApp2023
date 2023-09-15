import dash
from dash import html, callback, Input, Output
#from DashApp2023.apps import survey_unit_dropdown
from DashApp2023.apps import scatter_plot
from DashApp2023.apps import error_bar_plot
#from DashApp2023.apps import leaflet_map
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
dash.register_page(__name__, path='/main_dash')
layout = html.Div([
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        mapbox.layout,

                    ]),
                    width={'size': 12, 'offset': 0, 'buffer': 0}  # width number of cols out of 12 it takes up
                ),

                # Place the map layout here
                # leaflet_map.layout,


                # Add the Loading component with centered styling, the activation of this is found in the scatter plot
                html.Div(
                    dcc.Loading(
                        id="loading-spinner",
                        type="default",
                        children=[
                            html.Div(id="output-content"),
                        ],
                    ),
                    style={
                        "display": "flex",
                        "align-items": "center",  # Center vertically
                        "justify-content": "center",  # Center horizontally
                        "height": "50px",  # Set the desired height
                        "margin": "0px 0"  # Add margin for buffer
                    }
                ),

                # Create a new row for the "scatter_plot" and "error_bar_plot"
                dbc.Row( children=[
                    dbc.Col(
                        html.Div([
                            scatter_plot.layout,

                        ]),
                        width={'size': 6, 'offset': 0}
                    ),
                    dbc.Col(
                        html.Div([
                            error_bar_plot.layout,
                        ]),
                        width={'size': 6, 'offset': 0}
                    )]
                ),


                # Create a new row for the "Profile Line Plot" and "CSA_Table"
                dbc.Row( children=[
                    dbc.Col(
                        html.Div([
                            profile_line_plot.layout,

                        ]),
                        width={'size': 6, 'offset': 0}
                    ),
                    dbc.Col(
                        html.Div([
                            CSA_Table.layout,
                        ]),
                        width={'size': 6, 'offset': 0}
                    )]
                ),




            ],

            style={'display': 'flex', 'flex-wrap': 'wrap',}  # Use flexbox to control the layout
        ),

        fluid=True,  # Set fluid to True for a full-width container
        style={"width": "100%", 'text-align': 'center', 'margin-right': '150px',},
    )
])
