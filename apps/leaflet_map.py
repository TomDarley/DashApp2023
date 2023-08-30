import dash_leaflet as dl
from dash import Output, Input, html,callback,State,dcc
import psycopg2
import geopandas as gpd
import json
import dash
import plotly.express as px
from flask import jsonify
import dash_bootstrap_components as dbc
from dash_extensions.javascript import Namespace


# Define the center coordinates (latitude and longitude)
center_coordinates = [50.739315618362184, -3.9882308804193345]

# Establish database connection
conn = psycopg2.connect(
    database="Dash_DB",
    user="postgres",
    password="Plymouth_C0",
    host="localhost",
    port="5432"
)

# Import spatial data as GeoDataFrame
query = "SELECT * FROM survey_units"  # Modify this query according to your table
gdf = gpd.GeoDataFrame.from_postgis(query, conn, geom_col='wkb_geometry')
gdf = gdf.to_crs(epsg=4326)
# Close the database connection
conn.close()

# Convert to GeoJSON  format
geojson = gdf.to_json()
geojson = json.loads(geojson)

# Restructured GeoJSON data
restructured_geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Iterate through the original features and restructure them to be compatible with leaflet
for original_feature in geojson["features"]:
    restructured_feature = {
        "type": "Feature",
        "properties": {
            "sur_unit": original_feature["properties"]["sur_unit"]
        },
        "geometry": original_feature["geometry"]
    }
    restructured_geojson["features"].append(restructured_feature)

ns = Namespace("myNamespace", "mySubNamespace")

# Define the layout
layout = html.Div([

    dcc.Store(id='selected-value-storage', data={'current': None, 'previous': None}),

    # add dropdown with survey units to select
    dl.Map(children=[
        dl.TileLayer(),

        dl.GeoJSON(
            data=restructured_geojson,

            id="survey_units",
            zoomToBoundsOnClick=True,
            options={
                'pointToLayer': ns("pointToLayer")
            }
        ),
#
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"},
        id="map",
        center=[50.739315618362184, -3.9882308804193345],
        zoom=8),

])

# Callback stores the current selection on the map
@callback(
    Output('selected-value-storage', 'data'),
    Input('survey_units', 'click_feature'),
    prevent_initial_call=True
)
def update_selected_value(click_feature):
    """If map feature selected store the value in selected-value-storage else do nothing"""
    if click_feature:
        selected_value = click_feature['properties']['sur_unit']
        return selected_value
    else:
        return dash.no_update

@callback(
    Output('survey-unit-dropdown', 'value'),
    Input('selected-value-storage', 'data'),
    prevent_initial_call=True
)
def update_dropdown(selected_value):
    """If dropdown selected store the value in selected-value-storage"""
    return selected_value


@callback(
    Output('map', 'children'),
    Input('survey-unit-dropdown', 'value'),
    Input('survey_units', 'click_feature'),

    prevent_initial_call=True
)
def update_map(selected_value, click_feature):
    """If the click feature != dropdown selection we reload the geojson which removes the selection from the map """

    # You can update the GeoJSON data here based on the selected_value
    if click_feature:

        if selected_value != click_feature['properties']['sur_unit']:
            return [
                dl.TileLayer(),
                dl.GeoJSON(
                    data=restructured_geojson,
                    id="survey_units",
                    zoomToBoundsOnClick=True,
                    options={
                        'pointToLayer': ns("pointToLayer")
                    }
                ),
            ]
        else:

            return dash.no_update
    else:
        return dash.no_update






