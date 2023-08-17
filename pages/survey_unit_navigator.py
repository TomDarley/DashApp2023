import dash
from apps import leaflet_map
from dash import html, callback, Input, Output
from apps import survey_unit_dropdown
import dash_bootstrap_components as dbc

# register the page with dash giving url path
dash.register_page(__name__, path='/survey_unit_navigation')

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
                    width={'size': 11, 'offset': 1}  # width number of cols out of 12 it takes up
                ),
                survey_unit_dropdown.layout,
                # Place the map layout here
                leaflet_map.layout

            ],
            style={'display': 'flex', 'flex-wrap': 'wrap'}  # Use flexbox to control the layout
        ),
        style={'text-align': 'center'}
    ),

])


# Call back controls the selection of survey units from either the map or the dropdown
@callback(Output("survey-unit-dropdown", "value"), [Input("survey_units", "click_feature")])
def map_click(click_feature):
    if click_feature is not None:
        selected_value = click_feature['properties']['sur_unit']
        print(f"You clicked {click_feature['properties']['sur_unit']}")
    else:
        selected_value = '6aSU10'
    return selected_value
