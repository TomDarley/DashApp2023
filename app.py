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
app.layout = html.Div(children =
                      [navigation.navbar,
                       dash.page_container],
                      #style={'background-image': 'url("assets/abstract-smooth-blue-with-black-vignette-studio-well-use-as-backgroundbusiness-reportdigitalwebsite.jpg")',
                      #      'background-size': 'cover',
                      #      'background-repeat': 'no-repeat',
                      #      'background-position': 'fixed', 'height': '100vh'}
#

                      style ={'background': 'linear-gradient(to bottom right,#031437, #3C68C0)','background-color': 'black'}

)

print("Running Dash App")


if __name__ == "__main__":
    #app.run_server(host='0.0.0.0', port=8050, debug=True)
    app.run_server(debug=True)







