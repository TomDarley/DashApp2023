import dash_bootstrap_components as dbc

# bootstrap navigation bar imported into pages it can be used multiple times
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/home")),

        dbc.NavItem(dbc.NavLink("Survey Unit Navigation", href="/survey_unit_navigation")),
        dbc.NavItem(dbc.NavLink("Survey Log", href="/survey_data")),# add additional pages here
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",

        ),
    ],
    brand="SWCM Topo Dash",
    brand_href="https://southwest.coastalmonitoring.org/",
    color="primary",
    dark=True,
    fluid=True,
    links_left=True
)

