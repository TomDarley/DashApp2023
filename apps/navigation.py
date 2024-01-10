import dash_bootstrap_components as dbc
from dash import Input, Output, State, html,dcc,callback
from dash_bootstrap_components._components.Container import Container

PLOTLY_LOGO = "assets/Full-Logo (white sky).png"
# Define custom CSS style for navigation links
custom_navlink_style = {
    "font-size": "16px",
    "color": "white",'position': 'absolute','right': '10px','top': '10px'

    ## Adjust the font size as needed
}
search_bar = dbc.Row(
    [
        dbc.Col(),
        dbc.Col(
            dbc.NavItem(
                dbc.NavLink(
                    "SWCM Dash",
                    href="https://southwest.coastalmonitoring.org/",
                    style=custom_navlink_style,
                )
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px", style={'position': 'absolute','left': '10px','top': '5px'})),
                        dbc.Col(dcc.Loading(
                            id='test_loader',
                            children=[html.Div(".", style={
                                "backgroundColor": "rgba(0, 0, 0, 0)",
                                'width': '10px',
                                'height': '1px',
                                "zIndex": -1
                            })],
                            style={'position': 'fixed','top':'3%', 'left': '50%', 'transform': 'translate(-50%, -50%)'},


                            loading_state={'is_loading': True}
                        )),


                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://southwest.coastalmonitoring.org/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    style={'height': '50px'},
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