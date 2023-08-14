import dash
from dash import html, dcc
from pages import navigation

# register the page with dash giving url path
dash.register_page(__name__, path='/home')
layout = html.Div(children=[navigation.navbar,
                                  html.H1(children= "Hello")
                                  ])



