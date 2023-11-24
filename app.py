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
                        html.P("TDarley Applications © 2023", className="copyright"),
                    ],
                ),
            ]


        )

# Set the app layout with the navigation bar, the nav will be inherited by all pages
app.layout = html.Div(children =
                      [navigation.navbar,
                       dash.page_container,
                      ],

                      style ={'background': 'linear-gradient(to bottom right, #073b73,#7ebbfc)','background-color': 'white'}

)
# Append the footer to the main layout
app.layout.children.append(footer)
print("Running Dash App")


if __name__ == "__main__":
    #app.run_server(host='0.0.0.0', port=8050, debug=True)
    app.run_server(debug=True)







