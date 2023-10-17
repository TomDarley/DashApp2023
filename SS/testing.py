import dash
from dash import Output, Input, html, callback, dcc, State, ctx, callback_context
from sqlalchemy import create_engine
import geopandas as gpd
import plotly.express as px
from shapely.wkt import loads
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# All shapefile loaded into the database should not be promoted to multi
engine = create_engine("postgresql://postgres:Plymouth_C0@localhost:5432/Dash_DB")

# Connect to the database using the engine
conn = engine.connect()

# Import point (survey unit) spatial data as GeoDataFrame
query = "SELECT * FROM survey_units"  # Modify this query according to your table
gdf = gpd.GeoDataFrame.from_postgis(query, conn, geom_col="wkb_geometry")
gdf = gdf.to_crs(epsg=4326)
# Extract latitude and longitude from the geometry column
gdf["lat"] = gdf["wkb_geometry"].y
gdf["long"] = gdf["wkb_geometry"].x
gdf["size"] = 3
lon = gdf["wkb_geometry"]

set_survey_unit = "6aSU12"
set_profile_line = "6a01613"

# Set the color of the selected survey unit to red
gdf["color"] = ''
gdf['color'] = gdf['color'].astype(str)
gdf['color'] = gdf['sur_unit'].apply(lambda x: 'red' if x == set_survey_unit else 'blue') # the colors here are not set

# Extract the coordinates of the selected survey unit
selected_point = gdf.loc[gdf["sur_unit"] == set_survey_unit].iloc[0]
center_lat = selected_point["lat"]
center_lon = selected_point["long"]

scatter_trace = px.scatter_mapbox(
    gdf,
    lat="lat",
    lon="long",
    hover_name="sur_unit",
    hover_data=["sur_unit"],
    zoom=7,
    color_discrete_sequence=["#4459c2", "#eb05c4"],  #the colors are set here
    size="size",
    color="color",
    size_max=12,

)


scatter_trace.update_traces(marker=dict(colorscale='Viridis'))


# Get the line data from the database
query_profile_lines = f"SELECT * FROM sw_profiles WHERE surveyunit  = '6aSU12'"  # Modify this query according to your table
lines_gdf = gpd.GeoDataFrame.from_postgis(
    query_profile_lines, conn, geom_col="wkb_geometry"
)
lines_gdf = lines_gdf.to_crs(epsg=4326)
lines_gdf["type"] = "line"

# Extract individual WKT strings and create LineString geometries
line_data = gpd.GeoDataFrame(
    {"geometry": [loads(wkt) for wkt in lines_gdf["wkb_geometry"].astype("string")]}
)

line_traces =[]
# adding each WKT string as trace to the fig as a trace
for i, row in line_data.iterrows():
    line = row["geometry"]
    latitudes = [coord[1] for coord in line.coords]
    longitudes = [coord[0] for coord in line.coords]

    # Get the survey_unit value for this row
    profile_line_id = lines_gdf.iloc[i]["profname"]

    if set_profile_line == profile_line_id:
        colour = "#e8d90c"
        width = 8
    else:
        colour = "#246673"
        width = 5

    # Add the LineString trace to the map
    trace = px.line_mapbox(
        line_data,
        lat=latitudes,
        lon=longitudes,
        hover_name=[profile_line_id] * len(latitudes),

    )

    # Update the marker color
    trace.update_traces(line=dict(color=colour, width=width))

    line_traces.append(trace)


fig = go.Figure()

for i in range(len(line_traces)):
    fig.add_trace(line_traces[i].data[0])

# Add the scatter trace to the figure
fig.add_traces(scatter_trace.data)

fig.update_layout(mapbox_style="open-street-map")

# this removes white space around the map
fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
fig.update_traces(showlegend=False)


#fig.update_geos(center=dict(lat=5, lon=center_lon), projection=dict(scale =7))
# Set the center coordinates and zoom level
fig.update_layout(
    mapbox={
        "center": {"lat": center_lat, "lon": center_lon},
        "zoom": 14,
    }
)

fig.show()