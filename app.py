from dash import Dash,html,dcc, Input,Output
import dash
import dash_bootstrap_components as dbc
from apps import navigation


"""Main App page, all pages inherit from this one. Here we define the footer and add the top nav bar here. 
   We also add external stylesheets for bootstrap etc. We run the app from here. """

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
                      style ={'background-color': 'white'}

)

# Append the footer to the main layout
app.layout.children.append(footer)


@app.callback(
    Output('url', 'pathname'),
    [Input('url', 'pathname')]
)
def set_default_page(pathname):
    """
        Sets the default page to '/main_dash' if the current URL is None or '/'.

        This callback function is triggered when there is a change in the URL pathname. It checks if
        the pathname is None or '/' (root URL), indicating that the user is accessing the application
        for the first time or has landed on the root URL. In such cases, it redirects the user to
        '/main_dash'. Otherwise, it keeps the current URL pathname unchanged.

        Parameters:
            pathname (str): The current URL pathname.

        Returns:
            str: The updated URL pathname.
        """

    if pathname is None or pathname == '/':
        return '/main_dash'
    return pathname



if __name__ == "__main__":
    #app.run_server(host='0.0.0.0', port=8050, debug=False)
    app.run_server(debug=True)
    #app.run(port =8080)







