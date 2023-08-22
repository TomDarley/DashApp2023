import json
from dash import Dash, html, Input, Output, dcc, ClientsideFunction
import dash
import dash_bootstrap_components as dbc
#from retrying import retry
#from tenacity import wait_exponential, stop_after_attempt
#from sqlalchemy import text  # look into this for security Dash Docs!!!
from apps import navigation

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, dbc.icons.BOOTSTRAP])

# Set the app layout with the navigation bar, the nav will be inherited by all pages
app.layout = html.Div([
    navigation.navbar,
    dash.page_container])

if __name__ == '__main__':
    app.run(debug=True)
