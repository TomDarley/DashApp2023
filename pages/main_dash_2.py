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

                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Survey Unit:", className="card-title", style={'color': 'blue' ,'margin-bottom': '5px', }),
                            html.Div("6aSU12",id='survey_unit_card')

                        ])
                        ] , style={'margin': '10px'}),

                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Trend:", className="card-title", style={'color': 'blue' ,'margin-bottom': '5px' }),
                            html.Div("----",id='trend_card')

                        ])
                        ], style={'margin': '10px'}),

                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Highest Recorded CPA:", className="card-title", style={'color': 'blue' ,'margin-bottom': '5px' }),
                            html.Div("----",id='highest_card')

                        ])
                        ], style={'margin': '10px'}),

                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Lowest Recorded CPA:", className="card-title", style={'color': 'blue' ,'margin-bottom': '5px' }),
                            html.Div("----",id='lowest_card')

                        ])
                        ], style={'margin': '10px'}),


                ]),

                    xs = {"size": 12, "offset":0},
                    sm={"size": 12, "offset":0},
                    md = {"size": 12, "offset": 0},
                    lg = {"size": 2, "offset": 0},
                    xl = {"size": 2, "offset": 0},
                    xxl={"size": 2, "offset": 0},

                    align="start"



),

                dbc.Col(html.Div([
                    mapbox.layout,



                ],
                    style={ 'margin-top': '10px','height': '60vh'}),

                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size":5 , "offset": 0},),

                dbc.Col(html.Div(
                    scatter_plot.layout,


                ),  style={'margin-top': '10px', 'height': '100%', },
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0}),
            ],


            align="start",
            style= {}

        ),
    dbc.Row(
        [   dbc.Col(html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Download Charts:", className="card-title", style={'color': 'blue', 'margin-bottom': '10px', }),
                    dcc.RadioItems(
                        options=[
                            {'label': 'CPA Plot', 'value': 'cpa'},
                            {'label': 'Line Plot', 'value': 'line_plot'},
                            {'label': 'Box Plot', 'value': 'box_plot'}
                        ],)

                ])
            ], style={'margin': '20px', 'position': 'block'}),


        ]),  xs = {"size": 12, "offset":0},
                    sm={"size": 12, "offset":0},
                    md = {"size": 12, "offset": 0},
                    lg = {"size": 2, "offset": 0},
                    xl = {"size": 2, "offset": 0},
                    xxl={"size": 2, "offset": 0},
        align='start'),
            dbc.Col(html.Div(profile_line_plot.layout),  xs = {"size": 12, "offset":0},
                    sm={"size": 12, "offset":0},
                    md = {"size": 12, "offset": 0},
                    lg = {"size": 5, "offset": 0},
                    xl = {"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0}),

            dbc.Col(html.Div(error_bar_plot.layout), xs = {"size": 12, "offset":0},
                    sm={"size": 12, "offset":0},
                    md = {"size": 12, "offset": 0},
                    lg = {"size": 5, "offset": 0},
                    xl = {"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0}),

        ],
        align="start",),
    dbc.Row(
        [   dbc.Col(html.Div([ ]), xs = {"size": 12, "offset":0},
                    sm={"size": 12, "offset":0},
                    md = {"size": 12, "offset": 0},
                    lg = {"size": 2, "offset": 0},
                    xl = {"size": 2, "offset": 0},
                    xxl={"size": 2, "offset": 0}),
            dbc.Col(html.Div(CSA_Table.layout),  xs = {"size": 12, "offset":0},
                    sm={"size": 12, "offset":0},
                    md = {"size": 12, "offset": 0},
                    lg = {"size": 10, "offset": 0},
                    xl = {"size": 10, "offset": 0},
                    xxl={"size": 10, "offset": 0}),


        ],
        align="start", ),

    ])


@callback(
Output("survey_unit_card", "children"),
Input("survey-unit-dropdown", "value"),)

def update_survey_unit_card(current_sur_unit):
    if current_sur_unit:
        return current_sur_unit

@callback(
Output("trend_card", "children"),
Input("change_rate", "data"),)

def update_survey_unit_card(trend):
    print(trend)
    if trend:
        if "Accretion Rate" in trend:
            value = trend.split(':')[-1]
            comment = f" Accreting {value}"
            return html.Span(f"{comment}", style={'color': 'green'})
        elif "Erosion Rate" in trend:
            value = trend.split(':')[-1]
            comment = f" Eroding {value}"
            return html.Span(f"{comment}", style={'color': 'red'})
    else:
        return f"{trend}"



@callback(
Output("lowest_card", "children"),
Input("lowest_recorded_value", "data"),
Input("lowest_recorded_year", "data")
)

def update_survey_unit_card(lowest_data, lowest_year):
    if lowest_data and lowest_year:

        comment = f"{lowest_data} "
        return html.Span(f"{comment}", style={'color': 'red'})


@callback(
Output("highest_card", "children"),
Input("highest_recorded_value", "data"),
Input("highest_recorded_year", "data")
)

def update_survey_unit_card(highest_data, highest_year):
    if highest_data and highest_year:

        comment = f"{highest_data} "
        return html.Span(f"{comment}", style={'color': 'green'})