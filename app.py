from dash import Dash,html
import dash
import dash_bootstrap_components as dbc
from apps import navigation, csa_table, error_bar_plot, map_box_3, profile_line_plot,scatter_plot


# register the page with dash giving url path

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.COSMO,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        dbc.icons.BOOTSTRAP
    ],
)

# Set the app layout with the navigation bar, the nav will be inherited by all pages
app.layout = html.Div(
    [navigation.navbar, dash.page_container], style={"background-color": "#223055"},

)

print("Running Dash App")

if __name__ == "__main__":
    #app.run_server(host='0.0.0.0', port=8050, debug=True)
    app.run_server(debug=True)







