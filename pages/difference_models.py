import dash
from dash import html
from apps import navigation

dash.register_page(__name__, path= '/diff_models')

layout = html.Div(children=[
                            html.H1(children= "Coming Soon!")


                            ], style= {'background-color': 'white', 'text-align':'center'})