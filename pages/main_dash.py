import dash
from apps import leaflet_map
from dash import html, callback, Input, Output
from apps import survey_unit_dropdown
from apps import scatter_plot
from apps import error_bar_plot
import dash_bootstrap_components as dbc
from dash import dcc
import dash_leaflet as dl

# register the page with dash giving url path
dash.register_page(__name__, path='/main_dash')

layout = html.Div([
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H2(children="SWCM Dash", style={
                            'text-align': 'center',
                            'margin-top': '20px',
                            'font-size': '28px',
                            'font-weight': 'bold',
                            'color': 'white'
                        }),
                        html.P(
                            children=' Welcome to the South West Coastal Monitoring Topo Dash. '
                                     'From this page, you can select the specific survey unit you wish to display data for:'
                        ),

                        # Place the dropdown layout here

                    ]),
                    width={'size': 12, 'offset': 1}  # width number of cols out of 12 it takes up
                ),
                survey_unit_dropdown.layout,
                # Place the map layout here
                leaflet_map.layout,

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

            dbc.Col(
                    html.Div([
                        scatter_plot.layout,

                    ]),),
            dbc.Col(
                    html.Div([
                        error_bar_plot.layout,

                    ]),


            ),


            ],
            style={'display': 'flex', 'flex-wrap': 'wrap'}  # Use flexbox to control the layout
        ),
        style={'text-align': 'center'}
    ),

])







