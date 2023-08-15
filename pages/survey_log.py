import dash
from dash import html
from apps import navigation

dash.register_page(__name__, path= '/survey_data')

layout = html.Div(children=[
                            html.H1(children= "Survey Data Log Page")
                            ])