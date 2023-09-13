import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
import numpy as np
import pandas as pd
import psycopg2
import geopandas as gpd
from scipy.interpolate import interp1d
from datetime import datetime
import matplotlib.dates as mdates
import plotly.express as px
import statsmodels.api as sm
import plotly.graph_objs as go
import json
from sqlalchemy import create_engine


layout = html.Div(
    [
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="line_plot",
                        ),
                        width={"size": 12, "offset": 0, "order": 2},
                        style={
                            "margin-left": 0,
                            "margin-top": 10,
                            "background-colour": "white",
                        },
                    ),
                ]
            ),
            style={
                "background-color": "#1b1c1c",
                "margin": 0,  # Remove container margin
                "padding": 0,
            },  # Remove container padding
        )
    ]
)
@callback(
    (Output("line_plot", "figure")),
    [
     Input('survey-unit-dropdown', 'value'),
     Input('survey-line-dropdown', 'value')],
    prevent_initial_call=False)

def make_line_plot(selected_sur_unit, selected_profile):
    # All shapefile loaded into the database should not be promoted to multi
    engine = create_engine("postgresql://postgres:Plymouth_C0@localhost:5432/Dash_DB")
    # Connect to the database using the engine
    conn = engine.connect()

    # Load topo data from DB
    topo_query = f"SELECT * FROM topo_data WHERE survey_unit = '{selected_sur_unit}' AND reg_id = '{selected_profile}'"  # Modify this query according to your table
    topo_df = pd.read_sql_query(topo_query, conn)

    # Load master profile data from DB, extract chainage and elevation
    master_profile_chainage = []
    master_profile_elevation = []
    master_profile_query = f"SELECT * FROM master_profiles WHERE profile_id = '{selected_profile}'"
    mp_df = pd.read_sql_query(master_profile_query, conn)
    mp_df = mp_df.dropna(axis=1, how='any')
    for col in mp_df.columns[1:]:
        mp_df[col] = mp_df[col].str.split(',')
        first = mp_df[col][0][0]
        last = mp_df[col][0][-2]
        master_profile_chainage.append(first)
        master_profile_elevation.append(last)

    # Create a 2D line plot
    fig = px.line(topo_df, x='chainage', y='elevation_OD', color='date',
                  color_discrete_sequence=px.colors.qualitative.D3, template="plotly_dark")

    fig.add_trace(
        go.Scatter(x=master_profile_chainage, y=master_profile_elevation, line=dict(color='red', width=5, dash='dash'),
                   name='Master Profile')
    )

    # Customize x and y axis fonts and sizes
    fig.update_xaxes(
        title_text='Chainage (m)',
        title_font=dict(size=20, family='Helvetica'),  # Customize font size and family
        tickfont=dict(size=20, family='Helvetica')  # Customize tick font size and family
    )

    fig.update_yaxes(
        title_text='Elevation (m)',
        title_font=dict(size=20, family='Helvetica'),  # Customize font size and family
        tickfont=dict(size=20, family='Helvetica')  # Customize tick font size and family
    )

    # Customize the legend font and size
    fig.update_layout(
        legend=dict(
            title_font=dict(size=20, family='Helvetica'),  # Customize font size and family
            title_text='',  # Remove legend title
            font=dict(size=20, family='Helvetica')  # Customize font size and family for legend labels
        ),
        legend_traceorder='reversed',
        legend_title_text=f''
    )

    # Add a title to the plot
    fig.update_layout(title=f'{selected_profile}', title_font=dict(size=20, family='Helvetica'),title_x=0.5)




    return fig










