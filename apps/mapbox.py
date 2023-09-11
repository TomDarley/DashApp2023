import dash
from dash import Output, Input, html, callback, dcc,State

import gpd as gpd
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine
import geopandas as gpd
import plotly.express as px
from shapely.wkt import loads


# All shapefile loaded into the database should not be promoted to multi
engine = create_engine("postgresql://postgres:Plymouth_C0@localhost:5432/Dash_DB")

# Connect to the database using the engine
conn = engine.connect()

# Import spatial data as GeoDataFrame
query = "SELECT * FROM survey_units"  # Modify this query according to your table
gdf = gpd.GeoDataFrame.from_postgis(query, conn, geom_col="wkb_geometry")
gdf = gdf.to_crs(epsg=4326)
# Extract latitude and longitude from the geometry column
gdf['lat'] = gdf['wkb_geometry'].y
gdf['long'] = gdf['wkb_geometry'].x
gdf['size'] = 10
lon = gdf['wkb_geometry']

# Import spatial data as GeoDataFrame
query_profile_lines = "SELECT * FROM sw_profiles"  # Modify this query according to your table
lines_gdf = gpd.GeoDataFrame.from_postgis(query_profile_lines, conn, geom_col="wkb_geometry")
lines_gdf = lines_gdf.to_crs(epsg=4326)

# Extract individual WKT strings and create LineString geometries
line_data = gpd.GeoDataFrame(
    {'geometry': [loads(wkt) for wkt in lines_gdf['wkb_geometry'].astype("string")]}
)


fig = px.scatter_mapbox(gdf, lat="lat", lon="long", hover_name="sur_unit", hover_data=['sur_unit'],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300, size ='size')

for i, row in line_data.iterrows():
    line = row['geometry']
    latitudes = [coord[1] for coord in line.coords]
    longitudes = [coord[0] for coord in line.coords]

    # Add the LineString trace to the map
    fig.add_trace(px.line_mapbox(
        line_data,
        lat=latitudes,
        lon=longitudes,
    ).data[0])

fig.update_layout(mapbox_style="open-street-map")


layout = html.Div(children=[

    dcc.Graph(
        id='example-map',
        figure=fig,
        style={
                "width": "100%",
                "height": "50vh",
                "margin": "auto",
                "display": "block",

            }
    ),
])







## Convert to GeoJSON  format
#geojson = gdf.to_json()
#geojson = json.loads(geojson)
#
## Restructured GeoJSON data
#restructured_geojson = {"type": "FeatureCollection", "features": []}