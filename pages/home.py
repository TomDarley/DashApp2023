import dash
from pages import leaflet_map
from dash import html
import dash_bootstrap_components as dbc


# register the page with dash giving url path
dash.register_page(__name__)

layout = html.Div([

    dbc.Container(
        dbc.Row(
            dbc.Col(
                html.Div([
                    html.H2(children="SWCM Survey Unit Navigation Map", style={
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
                    leaflet_map.layout,
                ]),
                  # Center the column within the row
                    width={'size': 10, 'offset': 1}
            )
        )
    ,style={'text-align': 'center'})
])


