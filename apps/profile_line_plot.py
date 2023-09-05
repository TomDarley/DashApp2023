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
    # Import spatial data as GeoDataFrame
    query = f"SELECT * FROM topo_data WHERE survey_unit = '{selected_sur_unit}' AND reg_id = '{selected_profile}'"  # Modify this query according to your table
    df = pd.read_sql_query(query, conn)
    print(df)
    MLWS_Dict = {'6aSU1': '-1.3', '6aSU2': '-1.3', '6aSU3-2': '-1.65', '6aSU4': '-1.65',
                 '6aSU5-1': '-1.65',
                 '6aSU3-3': '-1.65',
                 '6aSU3': '-1.65',
                 '6aSU3-5': '-1.65',
                 '6aSU6-2': '-1.75',
                 '6aSU7-1': '-1.75',

                 '6aSU5-2': '-1.65', '6aSU5-3': '-1.75', '6aSU5-4': '-1.75', '6aSU5-5': '-1.75',
                 '6aSU6': '-1.75', '6aSU7': '-1.75', '6aSU8-1': '-1.75', '6aSU8-2': '-1.75', '6aSU9': '-1.75',
                 '6aSU10': '-1.94', '6aSU11': '-1.94', '6aSU12': '-1.94', '6aSU13': '-1.94', '6aSU14': '-1.94',
                 '6aSU15': '-1.94', '6aSU16-1': '-1.94', '6aSU16-2': '-1.13', '6bSU16-3': '-1.94',
                 '6bSU17': '-1.95', '6bSU18-1': '-1.95', '6bSU18-2': '-1.67', '6bSU19-1': '-1.95',
                 '6bSU19-2': '-1.95', '6bSU19-3': '-1.95', '6bSU19-4': '-1.95', '6bSU19-5': '-1.95',
                 '6bSU20-1': '-2.1', '6bSU20-2': '-2.02245967741936', '6bSU20-3': '-2.036',
                 '6bSU20-4': '-2.051', '6bSU21-1': '-2.064', '6bSU21-2': '-2.078', '6bSU21-3': '-2.092',
                 '6bSU21-4': '-2.107', '6bSU21-5': '-2.121', '6bSU21-6': '-2.135', '6bSU21-7': '-2.149',
                 '6bSU21-8': '-2.163', '6bSU21-9': '-2.177', '6bSU21-10': '-2.191', '6bSU21-11': '-2.205',
                 '6bSU22': '-2.02', '6bSU23': '-2.02', '6bSU24': '-2.02', '6bSU25-1': '-2.02',
                 '6bSU25-2': '-2.02', '6bSU25-3': '-2.02', '6bSU26-1': '-2.02', '6bSU26-2': '-2.02',
                 '6bSU26-3': '-2.02', '6cSU27': '-2.35', '6cSU28': '-2.35', '6cSU29': '-2.35',
                 '6cSU30-1': '-2.35', '6cSU30-2': '-2.35', '6cSU30-3': '-2.35', '6cSU30-4': '-2.35',
                 '6cSU30-5': '-2.35', '6cSU31-1': '-2.35', '6cSU31-2': '-2.35', '6cSU32-1': '-2.35',
                 '6cSU32-2': '-2.35', '6cSU32-3': '-2.35', '6cSU33': '-2.35', '6cSU34': '-2.35',
                 '6cSU35-1': '-2.42', '6cSU35-2': '-2.42', '6cSU35-3': '-2.42', '6cSU35-4': '-2.42',
                 '6cSU36': '-2.42', '6cSU37-1': '-2.42', '6cSU37-2': '-2.42', '6cSU37-3': '-2.42',
                 '6cSU38': '-2.42', '6cSU39': '-2.42', '6d6D1-1': '-2.42', '6d6D1-2': '-2.42',
                 '6d6D1-3': '-2.42', '6d6D1-4': '-2.45', '6d6D1-5': '-2.45', '6d6D1-6': '-2.45',
                 '6d6D1-7': '-2.45', '6d6D1-8': '-2.45', '6d6D1-9': '-2.45', '6d6D1-10': '-2.45',
                 '6d6D1-11': '-2.45', '6d6D1-12': '-2.45', '6d6D1-13': '-2.45', '6d6D2-1': '-2.45',
                 '6d6D2-2': '-2.45', '6d6D2-3': '-2.45', '6d6D2-4': '-2.45', '6d6D2-5': '-2.45',
                 '6d6D2-6': '-2.45', '6d6D2-7': '-2.45', '6d6D2-8': '-2.45', '6d6D2-9': '-2.45',
                 '6d6D2-10': '-2.45', '6d6D2-11': '-2.45', '6d6D2-12': '-2.35', '6d6D2-13': '-2.35',
                 '6d6D2-14': '-2.35', '6d6D2-15': '-2.35', '6d6D2-16': '-2.35', '6d6D2-17': '-2.35',
                 '6d6D2-18': '-2.35', '6d6D3-1': '-2.11', '6d6D3-2': '-2.11', '6d6D3-3': '-2.11',
                 '6d6D3-4': '-2.11', '6d6D3-5': '-2.11', '6d6D3-6': '-2.11', '6d6D3-7': '-2.11',
                 '6d6D3-8': '-2.11', '6d6D3-9': '-2.11', '6d6D3-10': '-2.11', '6d6D3-11': '-2.11',
                 '6d6D3-12': '-2.11', '6d6D3-13': '-2.11', '6d6D4-1': '-2.11', '6d6D5-1': '-2.11',
                 '6d6D5-2': '-2.11', '6d6D5-3': '-2.11', '6d6D5-4': '-2.11', '6d6D5-5': '-2.11',
                 '6d6D5-6': '-2.3', '6d6D5-7': '-2.3', '6d6D5-8': '-2.3', '6d6D5-9': '-2.3', '6d6D5-10': '-2.3',
                 '6d6D5-11': '-2.3', '6d6D5-12': '-2.3', '6d6D5-13': '-2.3', '6d6D5-14': '-2.3',
                 '6d6D5-15': '-2.3', '6d6D5-16': '-2.3', '6d6D5-17': '-2.3', '6d6D5-18': '-2.3',
                 '6eSU1': '-2.3', '6eSU2': '-2.3', '6eSU3-1': '-2.3', '6eSU3-2': '-2.3', '6eSU3-3': '-2.3',
                 '6eSU3-4': '-2.3', '6eSU3-5': '-2.3', '6eSU3-6': '-2.3', '6eSU3-7': '-2.3', '6eSU4-1': '-2.19',
                 '6eSU4-2': '-2.19', '6eSU4-3': '-2.19', '6eSU4-4': '-2.19', '6eSU4-5': '-2.19',
                 '6eSU4-6': '-2.19', '6eSU5': '-2.19', '6eSU6-1': '-2.19', '6eSU6-2': '-2.19',
                 '6eSU6-3': '-2.19', '6eSU6-4': '-2.19', '6eSU7': '-2.19', '6eSU8-1': '-2.25',
                 '6eSU8-2': '-2.25', '6eSU8-3': '-2.25', '6eSU9-1': '-2.25', '6eSU9-2': '-2.25',
                 '6eSU10-1': '-2.25', '6eSU10-2': '-2.25', '6eSU10-3': '-2.25', '6eSU11': '-2.25',
                 '6eSU12-1': '-2.25', '6eSU12-2': '-2.25', '6eSU13-1': '-2.25', '6eSU13-2': '-2.25',
                 '6eSU13-3': '-2.25', '6eSU14': '-2.25', '6eA1': '-2.21', '6eA2': '-2.21', '6eA3-1': '-2.21',
                 '6eA3-2': '-2.21', '6eA3-3': '-2.21', '6eA4-1': '-2.21', '6eA4-2': '-2.21', '6eA5': '-2.21',
                 '6eA6': '-2.21', '6eA7': '-2.21', '6eA8-1': '-2.21', '6eA8-2': '-2.21', '6eA8-3': '-2.21',
                 '6eA8-4': '-2.21', '6eB1-1': '-2.21', '6eB1-2': '-2.21', '6eB1-3': '-2.21', '6eB1-4': '-2.21',
                 '6eB1-5': '-2.21', '6eB1-6': '-2.21', '6eB2-1': '-2.21', '6eB2-2': '-2.21', '6eB2-3': '-2.21',
                 '6eB3-1': '-2.21', '6eB3-2': '-2.21', '6eB3-3': '-2.21', '6eB4': '-2.21', '6eM1-1': '-2.21',
                 '6eM1-2': '-2.21', '6eM1-3': '-2.21', '6eM1-4': '-2.21', '6eM2': '-2.21', '6eM3': '-2.21',
                 '6eM4': '-2.21', '6eM5': '-2.21', '6eM6': '-2.21', '6eM7': '-2.21', '6eM8': '-2.21',
                 '6eM9': '-2.21', '6eM10': '-2.21', '6eM11': '-2.21', '6eM12': '-2.21', '6eM13': '-2.21',
                 '6eM14': '-2.21', '6eM15': '-2.21', '6eM16-1': '-2.21', '6eM16-2': '-2.21', '6eM17': '-2.21',
                 '6eN1': '-2.21', '6eN2': '-2.21', '6eN3': '-2.21', '6eN4': '-2.21', '6eT1': '-2.21',
                 '6eT2': '-2.21', '6eT3-1': '-2.21', '6eT3-2': '-2.21', '6eT4': '-2.21', '6eT5': '-2.21',
                 '6eT6': '-2.21', '6eT7': '-2.21', '7a7A1-1': '-2.25', '7a7A1-2': '-2.25', '7a7A1-3': '-2.6',
                 '7a7A2-1': '-2.6', '7a7A2-2': '-2.6', '7a7A2-3': '-2.6', '7a7A2-4': '-2.6', '7a7A2-5': '-2.6',
                 '7a7A2-6': '-2.6', '7a7A2-7': '-2.6', '7a7A3-1': '-2.6', '7a7A3-2': '-2.6', '7a7A3-3': '-2.6',
                 '7a7A3-4': '-2.6', '7a7A3-5': '-2.6', '7a7A3-6': '-2.8', '7a7A3-7': '-2.8', '7a7A3-8': '-2.8',
                 '7a7A3-9': '-2.8', '7a7A3-10': '-2.8', '7a7A3-11': '-2.8', '7a7A3-12': '-3', '7a7A3-13': '-3',
                 '7a7A3-14': '-3', '7a7A3-15': '-3', '7a7A3-16': '-3', '7a7A3-17': '-3', '7a7A3-18': '-3',
                 '7a7A3-19': '-3', '7a7A3-20': '-3', '7a7A3-21': '-3', '7a7A3-22': '-3', '7a7A3-23': '-3',
                 '7a7A3-24': '-3', '7b7B1-1': '-3', '7b7B1-2': '-3', '7b7B1-3': '-3', '7b7B1-4': '-3',
                 '7b7B1-5': '-3', '7b7B1-6': '-3', '7b7B1-7': '-3', '7b7B1-8': '-3', '7b7B1-9': '-3',
                 '7b7B2-1': '-2.9', '7b7B2-2': '-2.9', '7b7B2-3': '-2.9', '7b7B2-4': '-2.9', '7b7B2-5': '-2.9',
                 '7b7B2-6': '-2.9', '7b7B2-7': '-2.9', '7b7B2-8': '-2.9', '7b7B2-9': '-2.9', '7b7B2-10': '-2.9',
                 '7b7B3-1': '-2.9', '7b7B3-2': '-2.9', '7b7B3-3': '-2.9', '7b7B3-4': '-2.9', '7b7B3-5': '-2.9',
                 '7cLUND1': '-3.5', '7cLUND2': '-3.5', '7cLUND3': '-3.5', '7cCLOV1': '-3.5', '7cCLOV2': '-3.5',
                 '7cCLOV3': '-3.5', '7cCLOV4': '-3.5', '7cCLOV5': '-3.5', '7cWEST1': '-2.98',
                 '7cWEST2': '-2.98', '7cWEST3': '-2.66', '7cWEST4': '-2.66', '7cAPPL1': '-2.66',
                 '7cAPPL2': '-2.66', '7cAPPL3': '-2.66', '7cINST1': '-2.66', '7cINST2': '-2.66',
                 '7cINST3': '-2.66', '7cINST4': '-2.66', '7cINST5': '-2.66', '7cSAUN1': '-2.98',
                 '7cSAUN2': '-2.98', '7cSAUN3': '-2.98', '7cCROY1': '-2.98', '7cCROY2': '-2.98',
                 '7cCROY3': '-2.98', '7cWOOL1': '-2.98', '7cWOOL2': '-2.98', '7cWOOL3': '-2.98',
                 '7cWOOL4-A': '-2.98', '7cWOOL4-B': '-2.98', '7cWOOL5': '-2.98', '7dLEE1': '-3.8',
                 '7dLEE2': '-3.8', '7dLEE3': '-3.8', '7dILFR1': '-3.8', '7dILFR2': '-3.8', '7dILFR3': '-3.8',
                 '7dILFR4': '-3.8', '7dILFR5': '-3.8', '7dILFR6': '-3.8', '7dILFR7': '-3.8', '7dLYNM1': '-3.8',
                 '7dLYNM2': '-4.3', '7dLYNM3': '-4.3', '7dFORE1': '-4.3', '7dFORE2': '-4.3', '7dPORL1': '-4.3',
                 '7dPORL2': '-4.3', '7dPORL3': '-4.3', '7dSELW1': '-4.4', '7dMINE1': '-4.4', '7dMINE2': '-4.4',
                 '7dMINE3': '-4.4', '7dMINE4': '-4.4', '7dMINE5': '-4.4', '7dMINE6': '-4.4', '7dWATC1': '-4.7',
                 '7dWATC2': '-4.7', '7dWATC3': '-4.7', '7dWATC4': '-4.7', '7dWATC5': '-4.7', '7dWATC6': '-4.7',
                 '7dWATC7': '-4.7', '7dLILS1': '-4.7', '7dLILS2': '-4.7', '7dLILS3': '-4.7', '7dPARR1': '-5.23',
                 '7dPARR2': '-5.23', '7dPARR3': '-5.23', '7dRBRUE': '-5.23', '7dBURN2': '-5.23',
                 '7dBURN3': '-5.23', '7dBURN4-A': '-5.23', '7dBURN4-B': '-5.23', '7dBURN5': '-5.2',
                 '7eWSM1': '-5.2', '7eWSM2': '-5.2', '7eSANB1': '-5.2', '7eSANB2': '-5.2'}

    df.to_csv(r'C:\Users\darle\PycharmProjects\Dash_App_Master\test_data.csv')
    # Create a 3D line plot
    fig = px.line(df, x='chainage', y='elevation_OD', color='date',template="plotly_dark",)

    # Customize the plot layout (optional)
    fig.update_layout(
        title='',
        scene=dict(
            xaxis_title='Chainage',
            yaxis_title='Elevation_OD',
            zaxis_title='Date',


        ),
    )




    return fig










