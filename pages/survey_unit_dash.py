import dash
from dash import html, dcc
from pages import navigation

dash.register_page(__name__, path='/survey_data')
layout = html.Div(children=[navigation.navbar,
                                  html.H1(children= "Data Page")
                                  ])