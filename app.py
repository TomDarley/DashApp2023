from dash import Dash,html,dcc, Input,Output
import dash
import dash_bootstrap_components as dbc
from apps import navigation
# Import the main_dash layout


# register the page with dash giving url path
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.COSMO,
        dbc.icons.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        dbc.icons.BOOTSTRAP,

    ],  # Set the default landing page URL with a trailing slash


)

# Footer content
footer = html.Div(
            className="footer-basic",
            children=[
                html.Footer(
                    children=[
                        html.Div(
                            className="social",
                            children=[
                                html.A(href="https://www.facebook.com/PlymouthCoastalObservatory/", children=[html.I(className="bi bi-facebook")]),
                                html.A(href="https://twitter.com/OfficialSWCM", children=[html.I(className="bi bi-twitter")]),
                                html.A(href="https://www.instagram.com/south.west.coastal.monitoring/", children=[html.I(className="bi bi-instagram")]),
                                html.A(href="https://www.linkedin.com/company/south-west-coastal-monitoring/", children=[html.I(className="bi bi-linkedin")]),
                            ],
                        ),
                        html.Ul(
                            className="list-inline",
                            children=[
                                html.Li(html.A("Home", href="#")),
                                html.Li(html.A("About", href="https://southwest.coastalmonitoring.org/about-us/")),
                                html.Li(html.A("Terms", href="https://southwest.coastalmonitoring.org/terms-and-conditions/")),
                                html.Li(html.A("Privacy Policy", href="https://southwest.coastalmonitoring.org/privacy-policy/")),
                            ],
                        ),
                        html.P("TDarley Applications © 2024", className="copyright"),
                    ],
                ),
            ]


        )

# Set the app layout with the navigation bar, the nav will be inherited by all pages
app.layout = html.Div(children =
                      [dcc.Location(id='url', refresh=True),
                       navigation.navbar,
                       dash.page_container,
                      ],
                      #'background': 'linear-gradient(to bottom right, #073b73,#7ebbfc)',
                      style ={'background-color': 'white'}

)

# Append the footer to the main layout
app.layout.children.append(footer)

print("Running Dash App")

@app.callback(
    Output('url', 'pathname'),
    [Input('url', 'pathname')]
)
def set_default_page(pathname):
    if pathname is None or pathname == '/':
        return '/main_dash'
    return pathname



if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8050, debug=False)
    #app.run_server(debug=True)
    #app.run(port =8080)







