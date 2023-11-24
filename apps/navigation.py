import dash_bootstrap_components as dbc
from dash import html

"""The main nav bar loaded into every page"""

# Define custom CSS style for navigation links
custom_navlink_style = {
    "font-size": "16px",
    "color": "white",
    ## Adjust the font size as needed
}

custom_brand_style = {"font-size": "20px", "font-color": "white"}

SWCM_LOGO = r"assets/Full-Logo (white sky).png"  # must be assets folder for some reason

navbar = html.Div(
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.NavbarSimple(
                        children=[
                            dbc.NavItem(
                                dbc.NavLink(
                                    "SWCM Dash",
                                    href="/main_dash",
                                    style=custom_navlink_style,
                                )
                            ),
                            #dbc.NavItem(
                            #   dbc.NavLink(
                            #       "Difference Models",
                            #       href="/diff_models",
                            #       style=custom_navlink_style,
                            #   )
                            #,  # add additional pages here
                        ],
                        brand=html.Img(
                            src=SWCM_LOGO,
                            style={
                                "height": "35px",
                            },
                        ),
                        brand_href="https://southwest.coastalmonitoring.org/",
                        color="#223055",
                        dark=True,
                        fluid=True,
                        links_left=False,
                        brand_style=custom_navlink_style,

                    )
                ]
            )
        ],
    ), style={'margin-bottom':'10px',  }
)
