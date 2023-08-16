import dash_leaflet as dl
from dash import Output, Input, html,callback
import psycopg2
import geopandas as gpd
import json
import dash
import plotly.express as px
from flask import jsonify
import dash_bootstrap_components as dbc


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

geojson= gdf.to_json()
geojson= json.loads(geojson)
print(geojson)


# Define the layout
layout = html.Div([
    dl.Map(children=[
        dl.TileLayer(),
        dl.GeoJSON(data=geojson, id="survey_unit_points",  zoomToBoundsOnClick=True)
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map"),
        dbc.Input(id="input", placeholder="Type something...", type="text"),
        html.Br(),
        html.P(id="capital"),


])



@callback(Output("capital", "children"), [Input("survey_unit_points", "click_feature")])
def map_click(click_feature):
    print(click_feature)
    if click_feature is not None:
        print(f"You clicked {click_feature['properties']['sur_unit']}")
        return f"You clicked {click_feature['properties']['sur_unit']}"



