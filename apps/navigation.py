import dash_bootstrap_components as dbc
from dash import html
"""The main nav bar loaded into every page"""

# Define custom CSS style for navigation links
custom_navlink_style = {
    "font-size": "25px"  # Adjust the font size as needed
}

custom_brand_style ={"font-size": "30px"}
SWCM_LOGO = r"https://southwest.coastalmonitoring.org/wp-content/themes/swrcmp/images/logo.png"


# bootstrap navigation bar imported into pages it can be used multiple times
navbar = dbc.NavbarSimple(
    children=[

        dbc.NavItem(dbc.NavLink("Home", href="/home",style=custom_navlink_style)),

        dbc.NavItem(dbc.NavLink("Dash", href="/main_dash2",style=custom_navlink_style)),
        dbc.NavItem(dbc.NavLink("Difference Models", href="/diff_models",style=custom_navlink_style)),# add additional pages here
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=False),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",style=custom_navlink_style

        ),
    dbc.Col(html.Img(src = SWCM_LOGO, height= "50px")),
    ],
    brand="SWCM Topo Dash",
    brand_href="https://southwest.coastalmonitoring.org/",
    color="primary",
    dark=True,
    fluid=True,
    links_left=False,
    brand_style=custom_navlink_style,


)

