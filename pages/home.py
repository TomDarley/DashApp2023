import dash
from apps import leaflet_map
from dash import html
import dash_bootstrap_components as dbc


# register the page with dash giving url path
dash.register_page(__name__, path='/home')

layout = html.Div([

    dbc.Container(
        dbc.Row(
            dbc.Col(
                html.Div([
                    html.H2(children="SWCM Topo Dash", style={
                        'text-align': 'center',
                        'margin-top': '20px',
                        'font-size': '28px',
                        'font-weight': 'bold',
                        'color': 'white'
                    }),
                    html.P(
                        children=' Welcome to the South West Coastal Monitoring Topo Dash. '
                                 'To get started click on the Survey Navigation Tab and select a survey unit to start '
                                 'interacting with the data '
                    ),

                ]),
                  # Center the column within the row
                    width={'size': 10, 'offset': 1}
            )
        )
    ,style={'text-align': 'center'})
],style={'text-align': 'center',  'background-size': 'cover'})


#'background-image': 'url("assets/swcm_logo.jpg")'