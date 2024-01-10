import dash_bootstrap_components as dbc
from dash import Input, Output, State, html,dcc,callback

PLOTLY_LOGO = "assets/Full-Logo (white sky).png"

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("SWCM Dash", className="ms-2",style={
                             'font-family': 'sans-serif',
                             'font-size': '20px',  # Adjust the size as needed
                             'color': 'your-font-color',
                         })),
                        dbc.Col(
                            dcc.Loading(
                                id='test_loader',
                                children=[html.Div("", style={
                                    "backgroundColor": "rgba(0, 0, 0, 0)",
                                    'width': '10px',
                                    'height': '1px',
                                    "zIndex": -1
                                })],
                                style={'position': 'fixed', 'margin-left': '50%'},
                                loading_state={'is_loading': True}
                            ),
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Home", href="https://southwest.coastalmonitoring.org")),
                    dbc.NavItem(dbc.NavLink("About", href="https://southwest.coastalmonitoring.org/about-us/")),
                    dbc.NavItem(dbc.NavLink("Terms", href="https://southwest.coastalmonitoring.org/terms-and-conditions/"))],className="ms-auto"
                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="#10335b",
    dark=True,
)

# add callback for toggling the collapse on small screens
@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open