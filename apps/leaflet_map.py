import dash_leaflet as dl
from dash import Output, Input, html,callback
import psycopg2
import geopandas as gpd
import json
import dash
import plotly.express as px
from flask import jsonify
import dash_bootstrap_components as dbc
from dash_extensions.javascript import Namespace

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

    # add drop down with survey units to select


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

    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map"),
        dbc.Input(id="input", placeholder="Type something...", type="text"),
        html.Br(),
        html.P(id="capital")
])





