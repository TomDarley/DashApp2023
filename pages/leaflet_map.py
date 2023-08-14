import dash_leaflet as dl
import pandas as pd
from dash import Output, Input
# Sample data for demonstration
data = [
    {'latitude': 37.7749, 'longitude': -122.4194, 'name': 'San Francisco'},
    {'latitude': 34.0522, 'longitude': -118.2437, 'name': 'Los Angeles'},
    {'latitude': 40.7128, 'longitude': -74.0060, 'name': 'New York'},
]
df = pd.DataFrame(data)
layout = dl.Map(dl.TileLayer(), style={'height': '80vh', 'width': '100%', 'buffer':'10px'})

