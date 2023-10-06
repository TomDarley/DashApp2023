import dash
from dash import html, callback, Input, Output

# from DashApp2023.apps import survey_unit_dropdown
from DashApp2023.apps import scatter_plot
from DashApp2023.apps import error_bar_plot

# from DashApp2023.apps import leaflet_map
from DashApp2023.apps import mapbox

from DashApp2023.apps import profile_line_plot
from DashApp2023.apps import csa_table
import dash_bootstrap_components as dbc
from dash import dcc
import psycopg2
import geopandas as gpd
import json
from dash_extensions.javascript import Namespace

# register the page with dash giving url path
dash.register_page(__name__, path="/main_dash")
layout = html.Div(
    [
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                mapbox.layout,
                            ]
                        ),
                        width={
                            "size": 9,
                            "offset": 0,
                            "buffer": 0,

                        },

                        style={"margin-bottom": "10px"}# width number of cols out of 12 it takes up
                    ),


                    dbc.Col(
                        html.Div(
                            [
                                dbc.Card(id="Survey_Unit_Label"),
                                dbc.CardBody(
                                    [
                                        html.H2("  Survey Unit:", className="card-title", style={'color': 'blue' ,'margin-bottom': '10px' }),
                                        dcc.Dropdown(
                                            options=[
                                                {'label': '6aSU10', 'value': '6aSU10'},
                                                {'label': '6aSU12', 'value': '6aSU12'},
                                                {'label': '6aSU13', 'value': '6aSU13'},
                                                {'label': '6aSU16-1', 'value': '6aSU16-1'},
                                                {'label': '6aSU2', 'value': '6aSU2'},
                                                {'label': '6aSU3-2', 'value': '6aSU3-2'},
                                                {'label': '6aSU3-3', 'value': '6aSU3-3'},
                                                {'label': '6aSU3-5', 'value': '6aSU3-5'},
                                                {'label': '6aSU4', 'value': '6aSU4'},
                                                {'label': '6aSU5-2', 'value': '6aSU5-2'},
                                                {'label': '6aSU5-4', 'value': '6aSU5-4'},
                                                {'label': '6aSU6-1', 'value': '6aSU6-1'},
                                                {'label': '6aSU6-2', 'value': '6aSU6-2'},
                                                {'label': '6aSU7-1', 'value': '6aSU7-1'},
                                                {'label': '6aSU8-1', 'value': '6aSU8-1'},
                                                {'label': '6bSU16-3', 'value': '6bSU16-3'},
                                                {'label': '6bSU17', 'value': '6bSU17'},
                                                {'label': '6bSU18-1', 'value': '6bSU18-1'},
                                                {'label': '6bSU18-2', 'value': '6bSU18-2'},
                                                {'label': '6bSU20-1', 'value': '6bSU20-1'},
                                                {'label': '6bSU21-2', 'value': '6bSU21-2'},
                                                {'label': '6bSU21-4', 'value': '6bSU21-4'},
                                                {'label': '6bSU21-5', 'value': '6bSU21-5'},
                                                {'label': '6bSU21-6', 'value': '6bSU21-6'},
                                                {'label': '6bSU21-8', 'value': '6bSU21-8'},
                                                {'label': '6bSU25-2', 'value': '6bSU25-2'},
                                                {'label': '6bSU26-1', 'value': '6bSU26-1'},
                                                {'label': '6bSU26-2', 'value': '6bSU26-2'},
                                                {'label': '6bSU26-3', 'value': '6bSU26-3'},
                                                {'label': '6cSU28', 'value': '6cSU28'},
                                                {'label': '6cSU30-2', 'value': '6cSU30-2'},
                                                {'label': '6cSU30-4', 'value': '6cSU30-4'},
                                                {'label': '6cSU31-1', 'value': '6cSU31-1'},
                                                {'label': '6cSU31-2', 'value': '6cSU31-2'},
                                                {'label': '6cSU31-3', 'value': '6cSU31-3'},
                                                {'label': '6cSU33', 'value': '6cSU33'},
                                                {'label': '6cSU38', 'value': '6cSU38'},
                                                {'label': '6d6D1-4', 'value': '6d6D1-4'},
                                                {'label': '6d6D1-6', 'value': '6d6D1-6'},
                                                {'label': '6d6D1-8', 'value': '6d6D1-8'},
                                                {'label': '6d6D2-13', 'value': '6d6D2-13'},
                                                {'label': '6d6D2-15', 'value': '6d6D2-15'},
                                                {'label': '6d6D2-17', 'value': '6d6D2-17'},
                                                {'label': '6d6D2-4', 'value': '6d6D2-4'},
                                                {'label': '6d6D2-7', 'value': '6d6D2-7'},
                                                {'label': '6d6D3-10', 'value': '6d6D3-10'},
                                                {'label': '6d6D3-12', 'value': '6d6D3-12'},
                                                {'label': '6d6D3-2', 'value': '6d6D3-2'},
                                                {'label': '6d6D3-4', 'value': '6d6D3-4'},
                                                {'label': '6d6D3-6', 'value': '6d6D3-6'},
                                                {'label': '6d6D5-10', 'value': '6d6D5-10'},
                                                {'label': '6d6D5-11', 'value': '6d6D5-11'},
                                                {'label': '6d6D5-12', 'value': '6d6D5-12'},
                                                {'label': '6d6D5-14', 'value': '6d6D5-14'},
                                                {'label': '6d6D5-15', 'value': '6d6D5-15'},
                                                {'label': '6d6D5-17', 'value': '6d6D5-17'},
                                                {'label': '6d6D5-2', 'value': '6d6D5-2'},
                                                {'label': '6d6D5-4', 'value': '6d6D5-4'},
                                                {'label': '6eSU10-1', 'value': '6eSU10-1'},
                                                {'label': '6eSU10-2', 'value': '6eSU10-2'},
                                                {'label': '6eSU11', 'value': '6eSU11'},
                                                {'label': '6eSU3-2', 'value': '6eSU3-2'},
                                                {'label': '6eSU3-4', 'value': '6eSU3-4'},
                                                {'label': '6eSU3-6', 'value': '6eSU3-6'},
                                                {'label': '6eSU4-3', 'value': '6eSU4-3'},
                                                {'label': '6eSU4-4', 'value': '6eSU4-4'},
                                                {'label': '6eSU4-5', 'value': '6eSU4-5'},
                                                {'label': '6eSU4-6', 'value': '6eSU4-6'},
                                                {'label': '6eSU4', 'value': '6eSU4'},
                                                {'label': '6eSU6-2', 'value': '6eSU6-2'},
                                                {'label': '6eSU8-2', 'value': '6eSU8-2'},
                                                {'label': '6eSU9-2', 'value': '6eSU9-2'},
                                                {'label': '7a7A1-2', 'value': '7a7A1-2'},
                                                {'label': '7a7A2-2', 'value': '7a7A2-2'},
                                                {'label': '7a7A2-3', 'value': '7a7A2-3'},
                                                {'label': '7a7A2-4', 'value': '7a7A2-4'},
                                                {'label': '7a7A2-5', 'value': '7a7A2-5'},
                                                {'label': '7a7A2-6', 'value': '7a7A2-6'},
                                                {'label': '7a7A2-7', 'value': '7a7A2-7'},
                                                {'label': '7a7A3-13', 'value': '7a7A3-13'},
                                                {'label': '7a7A3-15', 'value': '7a7A3-15'},
                                                {'label': '7a7A3-17', 'value': '7a7A3-17'},
                                                {'label': '7a7A3-18', 'value': '7a7A3-18'},
                                                {'label': '7a7A3-19', 'value': '7a7A3-19'},
                                                {'label': '7a7A3-2', 'value': '7a7A3-2'},
                                                {'label': '7a7A3-21', 'value': '7a7A3-21'},
                                                {'label': '7a7A3-23', 'value': '7a7A3-23'},
                                                {'label': '7a7A3-4', 'value': '7a7A3-4'},
                                                {'label': '7a7A3-8', 'value': '7a7A3-8'},
                                                {'label': '7a7A3-9', 'value': '7a7A3-9'},
                                                {'label': '7b7B1-2', 'value': '7b7B1-2'},
                                                {'label': '7b7B1-8', 'value': '7b7B1-8'},
                                                {'label': '7b7B2-4', 'value': '7b7B2-4'},
                                                {'label': '7b7B3-1', 'value': '7b7B3-1'},
                                                {'label': '7b7B3-2', 'value': '7b7B3-2'},
                                                {'label': '7b7B3-4', 'value': '7b7B3-4'},
                                                {'label': '7cSAUN1', 'value': '7cSAUN1'},
                                                {'label': '7cWEST2', 'value': '7cWEST2'},
                                                {'label': '7dBURN2', 'value': '7dBURN2'},
                                                {'label': '7dBURN3', 'value': '7dBURN3'},
                                                {'label': '7dBURN4-A', 'value': '7dBURN4-A'},
                                                {'label': '7dBURN4-B', 'value': '7dBURN4-B'},
                                                {'label': '7dLILS2', 'value': '7dLILS2'},
                                                {'label': '7dMINE1', 'value': '7dMINE1'},
                                                {'label': '7dMINE2', 'value': '7dMINE2'},
                                                {'label': '7dMINE3', 'value': '7dMINE3'},
                                                {'label': '7dMINE4', 'value': '7dMINE4'},
                                                {'label': '7dMINE5', 'value': '7dMINE5'},
                                                {'label': '7dMINE6', 'value': '7dMINE6'},
                                                {'label': '7dPARR2', 'value': '7dPARR2'},
                                                {'label': '7dPARR3', 'value': '7dPARR3'},
                                                {'label': '7dPORL1', 'value': '7dPORL1'},
                                                {'label': '7dPORL2', 'value': '7dPORL2'},
                                                {'label': '7dPORL3', 'value': '7dPORL3'},
                                                {'label': '7eSANB1', 'value': '7eSANB1'},
                                                {'label': '7eSU15-1', 'value': '7eSU15-1'},
                                                {'label': '7eSU15-2', 'value': '7eSU15-2'},
                                                {'label': '7eSU17-2', 'value': '7eSU17-2'},
                                                {'label': '7eSU17-5', 'value': '7eSU17-5'},
                                                {'label': '7eWSM1', 'value': '7eWSM1'},
                                                {'label': '7eWSM2', 'value': '7eWSM2'},
                                                {'label': '7eSAUN1', 'value': '7eSAUN1'},
                                                {'label': '6eA8-1', 'value': '6eA8-1'},
                                                {'label': '6eA8-2', 'value': '6eA8-2'},
                                                {'label': '6eA8-4', 'value': '6eA8-4'},
                                                {'label': '6eA4-2', 'value': '6eA4-2'},
                                                {'label': '6eM15', 'value': '6eM15'},
                                                {'label': '6eM12', 'value': '6eM12'},
                                                {'label': '6eM9', 'value': '6eM9'},
                                                {'label': '6eM7', 'value': '6eM7'},
                                                {'label': '6eM6', 'value': '6eM6'},
                                                {'label': '6eM5', 'value': '6eM5'},
                                                {'label': '6eM4', 'value': '6eM4'},
                                                {'label': '6eM3', 'value': '6eM3'},
                                                {'label': '6eM2', 'value': '6eM2'},
                                                {'label': '6eM1-3', 'value': '6eM1-3'},
                                                {'label': '6eM1-4', 'value': '6eM1-4'},
                                                {'label': '6eT6', 'value': '6eT6'},
                                                {'label': '6eT1', 'value': '6eT1'},
                                                {'label': '6eT7', 'value': '6eT7'},
                                                {'label': '6eT5', 'value': '6eT5'},
                                                {'label': '6eT4', 'value': '6eT4'},
                                                {'label': '6eT3-2', 'value': '6eT3-2'},
                                                {'label': '6eB3-1', 'value': '6eB3-1'},
                                                {'label': '6eB3-2', 'value': '6eB3-2'},
                                                {'label': '6eB1-1', 'value': '6eB1-1'},
                                                {'label': '6eB4', 'value': '6eB4'},
                                                {'label': '6eB1-4', 'value': '6eB1-4'},
                                                {'label': '6eB1-5', 'value': '6eB1-5'},
                                                {'label': '6eN1', 'value': '6eN1'},
                                                {'label': '6eN4', 'value': '6eN4'},
                                                {'label': '6eN3', 'value': '6eN3'},
                                                {'label': '6eN2', 'value': '6eN2'}],
                                            value='6aSU12',
                                            id='survey-unit-dropdown',
                                            style= {'font-size': '25px','margin':'0 auto'}


                                        ),

                                        html.H2("Profile Line:", className="card-title",
                                                style={'color': 'blue', }),
                                        dcc.Dropdown(
                                            options=['6a01613'],
                                            value='6a01613',
                                            id='survey-line-dropdown',
                                            style= {'font-size': '25px'}

                                        ),



                                    ]
                                ),
                            ],
                            style={
                                'display': 'flex',
                                'align-items': 'center',
                                "margin": "auto",
                                "marginTop": "20px",
                                "textAlign": "left",
                                "border": "1px solid #ccc",'background-color' :'#9de8f5'

                            },
                        ),

                        width={"size": 3, "offset":0},
                    ),


                    # Create a new row for the "scatter_plot" and "error_bar_plot"
                    dbc.Row(
                        children=[
                            dbc.Col(
                                html.Div(
                                    [
                                        scatter_plot.layout,
                                    ]
                                ),
                                width={"size": 6, "offset": 0},
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        error_bar_plot.layout,
                                    ]
                                ),
                                width={"size": 6, "offset": 0},
                            ),
                        ]
                    ),
                    # Create a new row for the "Profile Line Plot" and "CSA_Table"
                    dbc.Row(
                        children=[
                            dbc.Col(
                                html.Div(
                                    [
                                        profile_line_plot.layout,
                                    ]
                                ),
                                width={"size": 6, "offset": 0},
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        csa_table.layout,
                                    ]
                                ),
                                width={"size": 3, "offset": 6},
                            ),
                        ]
                    ),
                ],
                style={
                    "display": "flex",
                    "flex-wrap": "wrap",
                },  # Use flexbox to control the layout
            ),
            fluid=True,  # Set fluid to True for a full-width container
            style={
                "width": "100%",
                "text-align": "center",
                "margin-right": "150px",
            },
        )
    ]
)
