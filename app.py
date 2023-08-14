from dash import Dash, html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SOLAR, dbc.icons.BOOTSTRAP])
# Set the app layout with the navigation bar

if __name__ == '__main__':
    app.run(debug=True)
