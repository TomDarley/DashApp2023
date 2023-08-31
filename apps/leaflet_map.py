import dash_leaflet as dl
from dash import Output, Input, html, callback,  dcc
import psycopg2
import geopandas as gpd
import json
import dash
import plotly.express as px
from flask import jsonify
import dash_bootstrap_components as dbc
#from dash_extensions.javascript import Namespace, assign
from dash_extensions.javascript import assign
from sqlalchemy import create_engine




on_each_feature = assign("""function(feature, layer, context){
    if(feature.properties.sur_unit){  // don't bind anything for clusters (that do not have a city prop)
        layer.bindTooltip(`${feature.properties.sur_unit})`)
    }
}""")




point_to_layer = assign("""function(feature, latlng, context){
    
    var defaultMarkerOptions = {
                radius: 10,
                weight: 1,
                color: 'blue',
                fillColor: 'blue',
                fillOpacity: 0.6
            };
    var marker = L.circleMarker(latlng, defaultMarkerOptions);        
    return marker;;  // render a simple circle marker
}""")


#ns = Namespace("myNamespace", "mySubNamespace")


engine = create_engine('postgresql://postgres:Plymouth_C0@localhost:5432/Dash_DB')

# Connect to the database using the engine
conn = engine.connect()

# Import spatial data as GeoDataFrame
query = "SELECT * FROM survey_units"  # Modify this query according to your table
gdf = gpd.GeoDataFrame.from_postgis(query, conn, geom_col='wkb_geometry')
gdf = gdf.to_crs(epsg=4326)
# Close the database connection


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



## Import spatial data as GeoDataFrame
query_profile_lines = "SELECT * FROM sw_profiles"  # Modify this query according to your table
lines_gdf = gpd.GeoDataFrame.from_postgis(query_profile_lines, conn, geom_col='wkb_geometry')
lines_gdf = lines_gdf.to_crs(epsg=4326)

# Convert to GeoJSON  format
line_geojson = lines_gdf.to_json()
line_geojson = json.loads(line_geojson)


conn.close()


# Define the layout
layout = html.Div([

    dcc.Store(id='selected-value-storage', data={'current': None, 'previous': None}),

    # add dropdown with survey units to select
    dl.Map(children=[
        dl.TileLayer(),

        dl.GeoJSON(
            data=restructured_geojson,

            id="point_geojson",
            zoomToBounds=True,
            zoomToBoundsOnClick=True,

            options=
                dict(pointToLayer=point_to_layer, id="point_geojson",onEachFeature=on_each_feature,)

        ),




        #
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"},
        id="map",
        center=[50.739315618362184, -3.9882308804193345],
        zoom=8),
    dcc.Input(id = 'TEST')


])


@callback(Output("TEST", "value"), [Input("point_geojson", "click_feature")])
def capital_click(feature):
    if feature is not None:
        print(f"You clicked {feature['properties']['name']}")
        return f"You clicked {feature['properties']['name']}"












# Callback stores the current selection on the map
@callback(
    Output('selected-value-storage', 'data'),
    Input('point_geojson', 'click_feature'),
    prevent_initial_call=True,
)
def update_selected_value(click_feature):
    """If map feature selected store the value in selected-value-storage else do nothing"""
    if click_feature:
        selected_value = click_feature['properties'].get('sur_unit')
        print("Selected Value:", selected_value)
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
    print(f"Selected value storage set to: {selected_value}")
    return selected_value

@callback(
    Output('map', 'children'),
    Input('survey-unit-dropdown', 'value'),
    Input('point_geojson', 'click_feature'),

    prevent_initial_call=True
)
def update_map(selected_value, points_click_feature):
    """If the click feature != dropdown selection we reload the geojson which removes the selection from the map """

    # You can update the GeoJSON data here based on the selected_value
    if points_click_feature:
        print(points_click_feature['properties']['sur_unit'])
        if selected_value != points_click_feature['properties']['sur_unit']:
            return [
                dl.TileLayer(),
                dl.GeoJSON(
                    data=restructured_geojson,
                    id="point_geojson",
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
