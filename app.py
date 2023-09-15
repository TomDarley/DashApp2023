from dash import Dash, html, Input, Output, dcc, ClientsideFunction
import dash
import dash_bootstrap_components as dbc
from apps import navigation
from dash_extensions.javascript import Namespace

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.COSMO, dbc.icons.BOOTSTRAP,dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])

# Set the app layout with the navigation bar, the nav will be inherited by all pages
app.layout = html.Div([
    navigation.navbar,
    dash.page_container])

if __name__ == '__main__':
    app.run(debug=True)
