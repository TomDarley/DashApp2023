import dash
from dash import html, callback, Input, Output, State, dcc
from apps import scatter_plot
from apps import error_bar_plot
from apps import map_box_3
from apps import profile_line_plot
from apps import csa_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
import io
import plotly.io as pio
from sqlalchemy import create_engine
from io import StringIO
import json
from PIL import Image as PILImage
from datetime import datetime
from sqlalchemy.exc import OperationalError
import time
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Spacer, Paragraph,SimpleDocTemplate, Table, TableStyle,PageBreak, Image as PlatypusImage
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.units import mm
from PIL import Image, ImageDraw, ImageFont


"""This is the main page, all other apps are added to this page, it contains all the placeholders for the main layout. 
    This includes the the chart positions, the left hand side overview cards etc. This page also contains the report 
    generation function. Note that each chart/table is a separate app see apps folder."""

# generate the url for this page in the app
dash.register_page(__name__, path="/main_dash")


def establish_connection(retries=3, delay=5):
    """Function attempts to connect to the database. It will retry 3 times before giving up"""

    attempts = 0
    while attempts < retries:
        try:
            # Attempt to create an engine and connect to the database
            engine = create_engine(
                "postgresql://postgres:Plymouth_C0@swcm-dashboard.crh7kxty9yzh.eu-west-2.rds.amazonaws.com:5432/postgres"
            )
            conn = engine.connect()

            # If the connection is successful, return the connection object
            return conn

        except OperationalError as e:
            # Handle the case where a connection cannot be established
            print(f"Error connecting to the database: {e}")
            attempts += 1

            if attempts < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retry attempts reached. Giving up.")
                # Optionally, you can raise an exception, log the error, or take other appropriate actions

    return None  # Return None if all attempts fail


# define the layout of the main page
layout = html.Div(
    [
        # add download item, used for the report generation.
        dcc.Download(id="download"),

        # row one contains everything other than the lineplot and errorbar plot csa table
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(

                                        [
                                            html.Div("6aSU12", id='not-faded'),

                                        ]
                                    )
                                ],
                                id="survey_unit_card"

                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "  Search:",
                                                id="drop_down_card-title",

                                            ),

                                            dcc.Dropdown(
                                                options=[
                                                    {"label": "6aSU10  -  Sidmouth", "value": "6aSU10"},
                                                    {
                                                        "label": "6aSU12  -  Budleigh Salterton (East)",
                                                        "value": "6aSU12",
                                                    },
                                                    {
                                                        "label": "6aSU13  -  Budleigh Salterton",
                                                        "value": "6aSU13",
                                                    },
                                                    {"label": "6aSU16-1  -  Exmouth", "value": "6aSU16-1"},
                                                    {"label": "6aSU2  -  Chesil Beach", "value": "6aSU2"},
                                                    {
                                                        "label": "6aSU3-2  -  West Bexington",
                                                        "value": "6aSU3-2",
                                                    },
                                                    {"label": "6aSU3-3  -  The Hive", "value": "6aSU3-3"},
                                                    {
                                                        "label": "6aSU3-5  -  Burton Freshwater",
                                                        "value": "6aSU3-5",
                                                    },
                                                    {"label": "6aSU4  -  West Bay", "value": "6aSU4"},
                                                    {"label": "6aSU5-2  -  Seatown", "value": "6aSU5-2"},
                                                    {"label": "6aSU5-4  -  Charmouth", "value": "6aSU5-4"},
                                                    {
                                                        "label": "6aSU6-1  -  Lyme Regis (Broad Ledge)",
                                                        "value": "6aSU6-1",
                                                    },
                                                    {"label": "6aSU6-2  -  Lyme Regis", "value": "6aSU6-2"},
                                                    {"label": "6aSU7-1  -  The Cobb", "value": "6aSU7-1"},
                                                    {
                                                        "label": "6aSU8-1  -  Seaton (Devon)",
                                                        "value": "6aSU8-1",
                                                    },

                                                    {
                                                        "label": "6aSU8-2  -  Beer",
                                                        "value": "6aSU8-2",
                                                    },

                                                    {
                                                        "label": "6bSU16-3  -  Dawlish Warren",
                                                        "value": "6bSU16-3",
                                                    },
                                                    {"label": "6bSU17  -  Dawlish", "value": "6bSU17"},
                                                    {
                                                        "label": "6bSU18-1  -  Teignmouth",
                                                        "value": "6bSU18-1",
                                                    },
                                                    {
                                                        "label": "6bSU18-2  -  Teign Estuary",
                                                        "value": "6bSU18-2",
                                                    },
                                                    {
                                                        "label": "6bSU20-1  -  Oddicombe",
                                                        "value": "6bSU20-1",
                                                    },
                                                    {"label": "6bSU21-2  -  Meadfoot", "value": "6bSU21-2"},
                                                    {
                                                        "label": "6bSU21-4  -  Torquay and Livermead",
                                                        "value": "6bSU21-4",
                                                    },
                                                    {"label": "6bSU21-5  -  Paignton", "value": "6bSU21-5"},
                                                    {
                                                        "label": "6bSU21-6  -  Goodrington Sands",
                                                        "value": "6bSU21-6",
                                                    },
                                                    {
                                                        "label": "6bSU21-8  -  Broadsands",
                                                        "value": "6bSU21-8",
                                                    },
                                                    {
                                                        "label": "6bSU25-2  -  Blackpool Sands",
                                                        "value": "6bSU25-2",
                                                    },
                                                    {
                                                        "label": "6bSU26-1  -  Slapton Sands",
                                                        "value": "6bSU26-1",
                                                    },
                                                    {"label": "6bSU26-2  -  Beesands", "value": "6bSU26-2"},
                                                    {
                                                        "label": "6bSU26-3  -  Hallsands",
                                                        "value": "6bSU26-3",
                                                    },
                                                    {"label": "6cSU28  -  Salcombe", "value": "6cSU28"},
                                                    {
                                                        "label": "6cSU30-2  -  Hope Cove",
                                                        "value": "6cSU30-2",
                                                    },
                                                    {
                                                        "label": "6cSU30-3  -  Mouthwell",
                                                        "value": "6cSU30-3",
                                                    },

                                                    {
                                                        "label": "6cSU30-4  -  Thurlestone",
                                                        "value": "6cSU30-4",
                                                    },
                                                    {"label": "6cSU31-1  -  Bantham", "value": "6cSU31-1"},
                                                    {
                                                        "label": "6cSU31-2  -  Bigbury-on-Sea",
                                                        "value": "6cSU31-2",
                                                    },
                                                    {
                                                        "label": "6cSU31-3  -  Challaborough",
                                                        "value": "6cSU31-3",
                                                    },
                                                    {"label": "6cSU33  -  Wembury", "value": "6cSU33"},
                                                    {
                                                        "label": "6cSU38  -  Kingsand & Cawsand",
                                                        "value": "6cSU38",
                                                    },
                                                    {
                                                        "label": "6d6D1-4  -  Seaton (Cornwall) & Downderry",
                                                        "value": "6d6D1-4",
                                                    },
                                                    {"label": "6d6D1-6  -  Looe", "value": "6d6D1-6"},
                                                    {"label": "6d6D1-8  -  Talland", "value": "6d6D1-8"},
                                                    {
                                                        "label": "6d6D2-13  -  Pentewan Sands",
                                                        "value": "6d6D2-13",
                                                    },
                                                    {
                                                        "label": "6d6D2-15  -  Portmellon Beach",
                                                        "value": "6d6D2-15",
                                                    },
                                                    {
                                                        "label": "6d6D2-17  -  Gorran Haven",
                                                        "value": "6d6D2-17",
                                                    },
                                                    {"label": "6d6D2-4  -  Par Sands", "value": "6d6D2-4"},
                                                    {
                                                        "label": "6d6D2-7  -  Carlyon Bay",
                                                        "value": "6d6D2-7",
                                                    },
                                                    {
                                                        "label": "6d6D3-10  -  Carne Beach",
                                                        "value": "6d6D3-10",
                                                    },
                                                    {
                                                        "label": "6d6D3-12  -  Portscatho",
                                                        "value": "6d6D3-12",
                                                    },
                                                    {
                                                        "label": "6d6D3-2  -  Hemmick Beach",
                                                        "value": "6d6D3-2",
                                                    },
                                                    {
                                                        "label": "6d6D3-4  -  Porthluney Cove",
                                                        "value": "6d6D3-4",
                                                    },
                                                    {
                                                        "label": "6d6D3-6  -  Portholland",
                                                        "value": "6d6D3-6",
                                                    },
                                                    {
                                                        "label": "6d6D5-10  -  Porthallow",
                                                        "value": "6d6D5-10",
                                                    },
                                                    {
                                                        "label": "6d6D5-11  -  Porthoustock",
                                                        "value": "6d6D5-11",
                                                    },
                                                    {"label": "6d6D5-12  -  Coverack", "value": "6d6D5-12"},
                                                    {
                                                        "label": "6d6D5-14  -  Kennack Sands (East)",
                                                        "value": "6d6D5-14",
                                                    },
                                                    {
                                                        "label": "6d6D5-15  -  Kennack Sands (West)",
                                                        "value": "6d6D5-15",
                                                    },
                                                    {"label": "6d6D5-17  -  Cadgwith", "value": "6d6D5-17"},
                                                    {"label": "6d6D5-2  -  Swanpool", "value": "6d6D5-2"},
                                                    {"label": "6d6D5-4  -  Maenporth", "value": "6d6D5-4"},
                                                    {"label": "6eA4-2  -  The Bar", "value": "6eA4-2"},
                                                    {"label": "6eA8-1  -  Periglis", "value": "6eA8-1"},
                                                    {"label": "6eA8-2  -  Porth Coose", "value": "6eA8-2"},
                                                    {"label": "6eA8-4  -  Porth Killer", "value": "6eA8-4"},
                                                    {"label": "6eB1-1  -  Great Porth", "value": "6eB1-1"},
                                                    {
                                                        "label": "6eB1-2  -  Sinking Porth",
                                                        "value": "6eB1-2",
                                                    },
                                                    {
                                                        "label": "6eB1-4  -  Great Popplestones",
                                                        "value": "6eB1-4",
                                                    },
                                                    {
                                                        "label": "6eB1-5  -  Little Popplestones",
                                                        "value": "6eB1-5",
                                                    },
                                                    {
                                                        "label": "6eB2-2  -  Kitchen Porth",
                                                        "value": "6eB2-2",
                                                    },
                                                    {"label": "6eB3-1  -  The Town", "value": "6eB3-1"},
                                                    {
                                                        "label": "6eB3-2  -  Green Bay",
                                                        "value": "6eB3-2",
                                                    },
                                                    {
                                                        "label": "6eB3-3  -  Green Bay B",
                                                        "value": "6eB3-3",
                                                    },

                                                    {"label": "6eB4  -  Rushy Bay", "value": "6eB4"},
                                                    {"label": "6eM12  -  Old Town", "value": "6eM12"},
                                                    {"label": "6eM1-3  -  Hugh Town", "value": "6eM1-3"},
                                                    {"label": "6eM1-4  -  Hugh Town", "value": "6eM1-4"},
                                                    {"label": "6eM15  -  Porthcressa", "value": "6eM15"},
                                                    {"label": "6eM2  -  Porth Mellon", "value": "6eM2"},
                                                    {"label": "6eM3  -  Thomas' Porth", "value": "6eM3"},
                                                    {"label": "6eM4  -  Porth Loo", "value": "6eM4"},
                                                    {"label": "6eM5  -  Bar Point", "value": "6eM5"},
                                                    {"label": "6eM6  -  Pelistry", "value": "6eM6"},
                                                    {"label": "6eM7  -  Porth Hellick", "value": "6eM7"},
                                                    {"label": "6eM9  -  Porth Minnick", "value": "6eM9"},
                                                    {"label": "6eN1  -  Bab's Carn", "value": "6eN1"},
                                                    {"label": "6eN2  -  St Martin's Bay", "value": "6eN2"},
                                                    {"label": "6eN3  -  Higher Town Bay", "value": "6eN3"},
                                                    {
                                                        "label": "6eN4  -  St Martin's Flats",
                                                        "value": "6eN4",
                                                    },
                                                    {"label": "6eSU10-1  -  Marazion", "value": "6eSU10-1"},
                                                    {
                                                        "label": "6eSU10-2  -  Mounts Bay",
                                                        "value": "6eSU10-2",
                                                    },
                                                    {"label": "6eSU11  -  Newlyn", "value": "6eSU11"},
                                                    {"label": "6eSU3-2  -  Mullion", "value": "6eSU3-2"},
                                                    {"label": "6eSU3-4  -  Poldhu", "value": "6eSU3-4"},
                                                    {
                                                        "label": "6eSU3-6  -  Church Cove",
                                                        "value": "6eSU3-6",
                                                    },
                                                    {
                                                        "label": "6eSU4-3  -  Gunwalloe Cove",
                                                        "value": "6eSU4-3",
                                                    },
                                                    {"label": "6eSU4-4  -  Loe Bar", "value": "6eSU4-4"},
                                                    {
                                                        "label": "6eSU4-5  -  Porthleven Sands",
                                                        "value": "6eSU4-5",
                                                    },
                                                    {"label": "6eSU4-6  -  Porthleven", "value": "6eSU4-6"},
                                                    {"label": "6eSU6-2  -  Praa Sands", "value": "6eSU6-2"},
                                                    {
                                                        "label": "6eSU8-2  -  Perran Sands",
                                                        "value": "6eSU8-2",
                                                    },
                                                    {
                                                        "label": "6eSU9-2  -  Little London",
                                                        "value": "6eSU9-2",
                                                    },
                                                    {"label": "6eT1  -  New Grimsby", "value": "6eT1"},
                                                    {"label": "6eT3-2  -  Old Grimsby", "value": "6eT3-2"},
                                                    {"label": "6eT4  -  Borough Beach", "value": "6eT4"},
                                                    {"label": "6eT5  -  Pentle Bay", "value": "6eT5"},
                                                    {"label": "6eT6  -  Appletree Bay", "value": "6eT6"},
                                                    {"label": "6eT7  -  New Grimsby", "value": "6eT7"},
                                                    {
                                                        "label": "7a7A1-2  -  Sennen Cove",
                                                        "value": "7a7A1-2",
                                                    },
                                                    {
                                                        "label": "7a7A2-2  -  Porthmeor Beach",
                                                        "value": "7a7A2-2",
                                                    },
                                                    {
                                                        "label": "7a7A2-3  -  Porth Gwidden",
                                                        "value": "7a7A2-3",
                                                    },
                                                    {"label": "7a7A2-4  -  St Ives", "value": "7a7A2-4"},
                                                    {"label": "7a7A2-5  -  Carbis Bay", "value": "7a7A2-5"},
                                                    {
                                                        "label": "7a7A2-6  -  Hayle Estuary",
                                                        "value": "7a7A2-6",
                                                    },
                                                    {
                                                        "label": "7a7A2-7  -  Hayle Estuary to Godrevy Point",
                                                        "value": "7a7A2-7",
                                                    },
                                                    {
                                                        "label": "7a7A3-13  -  Crantock Beach",
                                                        "value": "7a7A3-13",
                                                    },
                                                    {
                                                        "label": "7a7A3-15  -  Fistral Beach",
                                                        "value": "7a7A3-15",
                                                    },
                                                    {
                                                        "label": "7a7A3-17  -  Newquay to Porth (Towan)",
                                                        "value": "7a7A3-17",
                                                    },
                                                    {
                                                        "label": "7a7A3-18  -  Watergate Bay",
                                                        "value": "7a7A3-18",
                                                    },
                                                    {"label": "7a7A3-19  -  Trenance", "value": "7a7A3-19"},
                                                    {"label": "7a7A3-2  -  Portreath", "value": "7a7A3-2"},
                                                    {
                                                        "label": "7a7A3-21  -  Porthcothan",
                                                        "value": "7a7A3-21",
                                                    },
                                                    {
                                                        "label": "7a7A3-23  -  Treyarnon & Constantine",
                                                        "value": "7a7A3-23",
                                                    },
                                                    {
                                                        "label": "7a7A3-4  -  Porth Towan",
                                                        "value": "7a7A3-4",
                                                    },
                                                    {
                                                        "label": "7a7A3-8  -  Perranporth",
                                                        "value": "7a7A3-8",
                                                    },
                                                    {
                                                        "label": "7a7A3-9  -  Perranporth Sands",
                                                        "value": "7a7A3-9",
                                                    },
                                                    {"label": "7b7B1-2  -  Harlyn", "value": "7b7B1-2"},
                                                    {"label": "7b7B1-8  -  Polzeath", "value": "7b7B1-8"},
                                                    {"label": "7b7B2-4  -  Port Isaac", "value": "7b7B2-4"},
                                                    {"label": "7b7B3-1  -  Black Rock", "value": "7b7B3-1"},
                                                    {
                                                        "label": "7b7B3-2  -  Widemouth Sand",
                                                        "value": "7b7B3-2",
                                                    },
                                                    {"label": "7b7B3-4  -  Bude", "value": "7b7B3-4"},
                                                    {"label": "7cINST2  -  Instow", "value": "7cINST2"},
                                                    {
                                                        "label": "7cSAUN1  -  Crow Point to Saunton Sands",
                                                        "value": "7cSAUN1",
                                                    },
                                                    {
                                                        "label": "7cWEST2  -  Westward Ho!",
                                                        "value": "7cWEST2",
                                                    },
                                                    {
                                                        "label": "7dBURN2  -  Burnham-on-sea",
                                                        "value": "7dBURN2",
                                                    },
                                                    {
                                                        "label": "7dBURN3  -  Berrow Dunes",
                                                        "value": "7dBURN3",
                                                    },
                                                    {
                                                        "label": "7dBURN4-A  -  Brean Village (South)",
                                                        "value": "7dBURN4-A",
                                                    },
                                                    {
                                                        "label": "7dBURN4-B  -  Brean Village (North)",
                                                        "value": "7dBURN4-B",
                                                    },
                                                    {"label": "7dLILS2  -  Lilstock", "value": "7dLILS2"},
                                                    {
                                                        "label": "7dMINE1  -  Culver Cliff to Minehead",
                                                        "value": "7dMINE1",
                                                    },
                                                    {
                                                        "label": "7dMINE2  -  Minehead Harbour to Warren Point",
                                                        "value": "7dMINE2",
                                                    },
                                                    {"label": "7dMINE3  -  The Warren", "value": "7dMINE3"},
                                                    {
                                                        "label": "7dMINE3b  -  The Warren",
                                                        "value": "7dMINE3b",
                                                    },
                                                    {
                                                        "label": "7dMINE4  -  Dunster Beach Holiday Park",
                                                        "value": "7dMINE4",
                                                    },
                                                    {"label": "7dMINE5  -  Ker Moor", "value": "7dMINE5"},
                                                    {"label": "7dMINE5b  -  Ker Moor", "value": "7dMINE5b"},
                                                    {
                                                        "label": "7dMINE6  -  Blue Anchor",
                                                        "value": "7dMINE6",
                                                    },
                                                    {
                                                        "label": "7dPARR2  -  Hinkley Point to Stolford",
                                                        "value": "7dPARR2",
                                                    },
                                                    {"label": "7dPARR3  -  Steart", "value": "7dPARR3"},
                                                    {"label": "7dPARR3b  -  Steart", "value": "7dPARR3b"},
                                                    {"label": "7dPARR3c  -  Steart", "value": "7dPARR3c"},
                                                    {
                                                        "label": "7dPORL1  -  Gore Point to Porlock Weir",
                                                        "value": "7dPORL1",
                                                    },
                                                    {
                                                        "label": "7dPORL2  -  Porlock Weir",
                                                        "value": "7dPORL2",
                                                    },
                                                    {
                                                        "label": "7dPORL3  -  Porlockford to Hurlstone Point",
                                                        "value": "7dPORL3",
                                                    },
                                                    {"label": "7eSANB1  -  Sand Bay", "value": "7eSANB1"},
                                                    {"label": "7eSANB1b  -  Sand Bay", "value": "7eSANB1b"},
                                                    {
                                                        "label": "7eSU15-1  -  Severn Beach",
                                                        "value": "7eSU15-1",
                                                    },
                                                    {
                                                        "label": "7eSU15-2  -  Avonmouth",
                                                        "value": "7eSU15-2",
                                                    },
                                                    {
                                                        "label": "7eSU17-2  -  Portishead",
                                                        "value": "7eSU17-2",
                                                    },
                                                    {"label": "7eSU17-5  -  Clevedon", "value": "7eSU17-5"},
                                                    {
                                                        "label": "7eWSM1  -  Weston-super-Mare",
                                                        "value": "7eWSM1",
                                                    },
                                                    {
                                                        "label": "7eWSM2  -  Weston-super-Mare",
                                                        "value": "7eWSM2",
                                                    },
                                                ],
                                                value="6aSU12",
                                                id="survey-unit-dropdown",

                                            ),

                                            dcc.Dropdown(
                                                options=[
                                                    # Showing interims only!
                                                    {'label': "6a01615", 'value': "6a01615"},
                                                    {'label': "6a01618", 'value': "6a01618"},
                                                    {'label': "6a01621", 'value': "6a01621"},
                                                    {'label': "6a01624", 'value': "6a01624"}],
                                                value="6a01613",
                                                id="survey-line-dropdown",

                                            ),
                                            dcc.Dropdown(
                                                # Now set to only have interims as a choice
                                                options=[

                                                    {
                                                        "label": "Interim Surveys",
                                                        "value": "Interim",
                                                    },

                                                ],
                                                value="Interim",
                                                id="survey-type-dropdown",
                                                multi=False

                                            ),
                                        ],
                                    )
                                ],

                                id="drop_down_card",

                            ),

                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Overall Trend:",
                                                className="card-title",
                                                style={
                                                    "color": "blue",
                                                    "margin-bottom": "5px",
                                                    "font-weight": 'bold'

                                                },
                                            ),
                                            html.Div("----", id="trend_card", style={"color": 'black'}),
                                            dbc.Button(
                                                [html.Span(className="bi bi-info-circle-fill")],
                                                size="sm",
                                                id="overall_trend_open_info",
                                                n_clicks=0,
                                                className="mr-3",
                                                style={"position": "absolute", "top": "8px", "right": "8px",
                                                       "border-radius": "5px"},
                                            ),

                                        ]
                                    )
                                ], id='trend_card_div',

                            ),

                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Percent Change:",
                                                className="card-title",
                                                style={
                                                    "color": "blue",
                                                    "margin-bottom": "5px",
                                                    "font-weight": 'bold'

                                                },
                                            ),
                                            html.Div("----", id="trend_card1"),
                                            dbc.Button(
                                                [html.Span(className="bi bi-info-circle-fill")],
                                                size="sm",
                                                id="percent_change_open_info",
                                                n_clicks=0,
                                                className="mr-3",
                                                style={"position": "absolute", "top": "8px", "right": "8px",
                                                       "border-radius": "5px"},
                                            ),
                                        ]
                                    )
                                ], id='trend_card_div',

                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Highest CPA:",
                                                className="card-title",
                                                style={
                                                    "color": "blue",
                                                    "margin-bottom": "5px",
                                                    "font-weight": 'bold'

                                                },
                                            ),
                                            html.Div("----", id="highest_card"),
                                        ]
                                    )
                                ], id='highest_card_div'

                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Lowest CPA:",
                                                className="card-title",
                                                style={
                                                    "color": "blue",
                                                    "margin-bottom": "5px",
                                                    "font-weight": 'bold'
                                                },
                                            ),
                                            html.Div("----", id="lowest_card"),
                                        ]
                                    )
                                ], id='lowest_card_div',

                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Report:",
                                                id="report-card-title",
                                                style={
                                                    "color": "blue",
                                                    "margin-bottom": "10px",
                                                    "font-weight": 'bold'

                                                },
                                            ),

                                            dcc.Loading(
                                                id='report_gen_loader',
                                                children=[dbc.Button(
                                                    "Generate Report",
                                                    id="download-charts-button",
                                                    n_clicks=0,
                                                    size="sm",
                                                    style={"border-radius": "10px"},
                                                    className='mr-3',
                                                ),
                                                ],
                                                style={'display': 'flex', 'justify-content': 'right', },
                                                loading_state={'is_loading': True},
                                                type="circle",
                                            ),

                                            # dcc.Checklist(
                                            #    id="download-check-list",
                                            #    options=[
                                            #        {
                                            #            "label": " CPA Plot ",
                                            #            "value": "cpa",
                                            #        },
                                            #        {
                                            #            "label": " CSL Plot ",
                                            #            "value": "line_plot",
                                            #        },
                                            #        {
                                            #            "label": " Box Plot",
                                            #            "value": "box_plot",
                                            #        },
                                            #    ],
                                            #    value=['cpa','line_plot','box_plot'],
                                            #    labelStyle={"margin-right": "10px"},
                                            #    style={"color": "#045F36", "font-weight": "bold", "font-size": "15px"},
                                            #    # inline=True,

                                            # ),



                                        ],
                                    )
                                ],
                                style={
                                    "margin": "10px",
                                    "position": "block",
                                    "border-radius": "10px",
                                    'box-shadow': '5px 5px 5px lightblue'
                                },
                            ),
                        ]
                    ), id='all_cards_div',
                    xs={"size": 12, "offset": 0, "overflow-y": "auto"},
                    sm={"size": 12, "offset": 0, "overflow-y": "auto"},
                    md={"size": 12, "offset": 0},
                    lg={"size": 2, "offset": 0},
                    xl={"size": 2, "offset": 0},
                    xxl={"size": 2, "offset": 0},
                    align="start",

                ),
                dbc.Col(

                    html.Div(
                        [

                            map_box_3.layout,

                        ],
                        id="main_dash_map_div",

                    ),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0},
                ),
                dbc.Col(
                    html.Div(

                        scatter_plot.layout,
                    ),
                    id='main_dash_scatter_div',

                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0},
                ),
            ],
            align="start",
        ),

        # row two contains  lineplot and errorbar plot
        dbc.Row(
            [
                dbc.Col(
                    html.Div([]),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 2, "offset": 0},
                    xl={"size": 2, "offset": 0},
                    xxl={"size": 2, "offset": 0},
                    align="start",
                ),
                dbc.Col(
                    html.Div([

                        # This is the alert message for when mp data only has one point.
                        dbc.Alert(
                            "Master Profile Data For This Profile Was Not Found, Please Try Another Profile!",
                            id="mp-alert",
                            is_open=False,
                            # duration=4000,
                            color="danger",
                            style={'position': 'absolute', 'top': '0', 'left': '0', 'right': '0', 'zIndex': 1000}
                        ),

                        profile_line_plot.layout,

                    ], style={'position': 'relative'}),

                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0},
                    id='main_dash_line_div',
                ),
                dbc.Col(
                    html.Div(error_bar_plot.layout),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0},

                ),
            ],

            id='main_dash_error_bar_div'
        ),

        # row three contains csa tables
        dbc.Row(
            [
                dbc.Col(
                    html.Div([]),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 2, "offset": 0},
                    xl={"size": 2, "offset": 0},
                    xxl={"size": 2, "offset": 0},

                    # style={'padding-right': '50px'}

                ),
                dbc.Col(
                    html.Div(csa_table.layout),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 10, "offset": 0},
                    xl={"size": 10, "offset": 0},
                    xxl={"size": 10, "offset": 0},

                    id='main_dash_csa_tables'

                ),
            ],

        ),

        # define the information  modals for the overall and percent change
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Overall Trend",
                                               style={"color": "blue"})),
                dbc.ModalBody(
                    [
                        html.P(
                            """The overall trend is a calculated by first determining the slope of a 
                            linear regression line fitted to the CPA (combined profile area) data. The slope
                             is then multiplied by 365 to convert it into an annual rate.""",
                            style={"font-size": 20}),

                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="overall_trend_info_close",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="overall_trend_info_model",
            is_open=False,
            fullscreen=False,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Percent Change (PCT)",
                                               style={"color": "blue"})),
                dbc.ModalBody(
                    [
                        html.P(
                            """Percentage change is determined by computing the absolute value of the difference between the total value of the first available CPA (Combined Profile Area) date and dividing it by the value of the most recent CPA date. This result is then multiplied by 100 to represent it as a percentage. When the maps PCT checkbox is activated, this calculation is adjusted to compare the most recent Spring CPA date value with the previous Spring CPA value.
                           """,
                            style={"font-size": 20}, ),

                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="percent_change_info_close",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="percent_change_info_model",
            is_open=False,
            fullscreen=False,
        ),
    ],
)


@callback(
    Output("survey_unit_card", "children"),
    Input("survey-unit-dropdown", "value"),
    State("survey-unit-dropdown", "options"),

)
def update_survey_unit_card(current_sur_unit, current_sur_unit_state):
    """
     Callback function to populate the survey unit CPA card with the currently selected survey unit.

     Parameters:
         current_sur_unit (str): The value of the currently selected survey unit from the dropdown.
         current_sur_unit_state (list): The options of the survey unit dropdown.

     Returns:
         str: The label corresponding to the selected survey unit to be displayed in the survey unit CPA card.
     """

    if current_sur_unit:
        label = [
            x["label"] for x in current_sur_unit_state if x["value"] == current_sur_unit
        ]

        label = label[0].split(" -")[1].strip()

        return label


@callback(
    Output("trend_card", "children"),

    Input("change_rate", "data"),

)
def update_trend_card(trend):
    """
    Callback function to grab the trend data from the change rate store found in the scatter plot page
    and format the output string.

    Parameters:
        trend (str): The trend data obtained from the change rate store in the scatter plot page.

    Returns:
        html.Span or str: If trend data is available, returns a formatted string indicating whether
        it represents an accretion rate or an erosion rate, along with the corresponding value.
        If no trend data is available, returns the original trend string.
    """

    if trend:
        if "Accretion Rate" in trend:
            value = trend.split(":")[-1]
            comment = f" Accreting {value}"
            return html.Span(f"{comment}", style={"color": 'green'})

        elif "Erosion Rate" in trend:
            value = trend.split(":")[-1]
            comment = f" Eroding {value}"
            return html.Span(f"{comment}", style={"color": 'red'})

    else:
        return f"{trend}"


@callback(
    Output("trend_card1", "children"),
    Input("survey-points-change-values", 'data'),  #
    State('change_range_radio_button', 'value')
)
def update_percent_change_card(change_value, change_range_radio_button):
    """
     Callback function to update the percent change card based on the survey unit selected
     CPA change between either the baseline to spring or spring to spring selection.

     Parameters:
         change_value (str): JSON string containing the change values.
         change_range_radio_button (str): The value of the change range radio button.

     Returns:
         html.Span or str: Depending on the classification of the change value and the selected range,
         returns a formatted string indicating the percent change along with its classification color,
         or returns a string indicating no change.
     """
    # Load JSON into DataFrame
    with StringIO(change_value) as json_data:
        change_values = pd.read_json(json_data)

    classification = list(change_values['features'])[0]
    classification_string = classification['properties']['classification']
    percent_change = round(classification['properties']['difference'], 2)

    color_mapping = {
        'High Erosion': "#ff0000",
        'Mild Erosion': "#ff6666",
        'Low Erosion': "#ff9999",
        'No Change': "#4f4f54",
        'Low Accretion': "#00ace6",
        'Mild Accretion': "#34c3eb",
        'High Accretion': "rgb(0, 57, 128)",
        'Selected Unit': "#ffff05"
    }
    color_to_use = color_mapping[classification_string]

    if classification_string in ['High Erosion', 'Mild Erosion', 'Low Erosion']:
        value = percent_change
        if change_range_radio_button == 'base-spr':
            comment = f"{value} %"
        else:
            comment = f"{value} %"

        return html.Span(f"{comment}", style={"color": color_to_use})

    elif classification_string in ['High Accretion', 'Mild Accretion', 'Low Accretion']:
        value = percent_change
        if change_range_radio_button == 'base-spr':
            comment = f"+ {value} %"
        else:
            comment = f"+ {value} %"

        return html.Span(f"{comment}", style={"color": color_to_use})

    elif classification_string == 'No Change':
        value = str(percent_change).strip("-")
        comment = f" +/- {value} %"

        return comment


@callback(
    Output("lowest_card", "children"),
    Input("lowest_recorded_value", "data"),
    Input("lowest_recorded_year", "data"),
)
def update_lowest_cpa_card(lowest_data, lowest_year):

    """
        Callback function to update the lowest CPA card. Grabs the data from the stores in the scatter plot page.

        Parameters:
            lowest_data (str): The lowest recorded CPA value.
            lowest_year (str): The year corresponding to the lowest recorded CPA value.

        Returns:
            html.Span or None: If both lowest_data and lowest_year are provided, returns a formatted string
            indicating the lowest CPA value. Otherwise, returns None.
        """

    if lowest_data and lowest_year:
        comment = f"{lowest_data} "
        return html.Span(f"{comment}", style={"color": "red"})


@callback(
    Output("highest_card", "children"),
    Input("highest_recorded_value", "data"),
    Input("highest_recorded_year", "data"),
)
def update_highest_cpa_card(highest_data, highest_year):
    """
       Callback function to update the highest CPA card. Grabs the data from the stores in the scatter plot page.

       Parameters:
           highest_data (str): The highest recorded CPA value.
           highest_year (str): The year corresponding to the highest recorded CPA value.

       Returns:
           html.Span or None: If both highest_data and highest_year are provided, returns a formatted string
           indicating the highest CPA value. Otherwise, returns None.
       """
    if highest_data and highest_year:
        comment = f"{highest_data} "
        return html.Span(f"{comment}", style={"color": "green"})


@callback(

    Output("download", "data"),
    Output('report_gen_loader', "loading_state"),
    Input("download-charts-button", "n_clicks"),
    # State("download-check-list", "value"),
    State("scatter_chart", "data"),
    State("error_chart", "data"),
    State("line_chart", "data"),
    State("survey_unit_card", "children"),
    State("survey-unit-dropdown", "value"),
    State("trend_card", "children"),
    State("highest_card", "children"),
    State("lowest_card", "children"),
    State("highest_recorded_year", "data"),  # these need switching they are the values not the dates
    State("lowest_recorded_year", "data"),

    State("spr_to_spr_table", "data"),
    State("spr_to_baseline_table", "data"),
    State('csa_header_store', "data"),
    State('percent_change', "data"),
    State('survey-line-dropdown', "value"),
    State('example-map', 'figure'),

    prevent_initial_call=True,
)
def generate_report(
        n_clicks, scatter_chart, error_chart, line_chart,
        sur_unit_card, current_survey_unit, trend, highest_date, lowest_date, highest_val, lowest_val, spr_to_spr_table,
        spr_to_baseline_table, csa_table_headers, percent_change, selected_profile, map_figure):

    """
    Function auto generates the report for download. It is hooking into data stores populated throughout the app
    and using report labs to build a pdf .

    Parameters:
        n_clicks (int): The number of times the download button has been clicked.
        scatter_chart (dict): Data for scatter chart.
        error_chart (dict): Data for error chart.
        line_chart (dict): Data for line chart.
        sur_unit_card (str): Content for the survey unit card.
        current_survey_unit (str): The currently selected survey unit.
        trend (dict): Content for the trend card.
        highest_date (dict): The highest recorded year.
        lowest_date (dict): The lowest recorded year.
        highest_val (float): The highest recorded value.
        lowest_val (float): The lowest recorded value.
        spr_to_spr_table (list): Data for the spring-to-spring table. List of dicts.
        spr_to_baseline_table (list): Data for the spring-to-baseline table. List of dicts.
        csa_table_headers (dicts): Data for CSA table headers.
        percent_change (str): Data for percent change.
        selected_profile (str): The selected profile.
        map_figure (dict): Figure data for the map.

    Returns:
        tuple: A tuple containing PDF data and loading state for the report generation.The pdf is sent to the dcc
        download using send bytes, this triggers the download in the browser to fire.
    """

    if n_clicks is None:
        raise PreventUpdate

    if n_clicks is None:
        return dash.no_update
    else:

        def to_pdf():

            # create a buffer in memory to store data
            buffer = io.BytesIO()

            # create a doc object using report labs default template
            doc = SimpleDocTemplate(buffer, pagesize=A4)


            def header(canvas, doc):
                """
                 Function to draw the header of the PDF document.

                 Parameters:
                     canvas (Canvas): The canvas object to draw on.
                     doc (SimpleDocTemplate): The document object representing the PDF.

                 Returns:
                     None
                 """

                # Get the current date and time
                current_datetime = datetime.now()

                # Convert the datetime object to a string
                current_datetime_str = current_datetime.strftime("%Y-%m-%d")

                canvas.saveState()
                canvas.setFont("Helvetica", 10)
                canvas.setFillColor(colors.grey)

                # Define the width of the page
                page_width, _ = A4

                # Calculate the position for the text to be on the right-hand side
                text_width = canvas.stringWidth(f"SWCM Generated Report {current_datetime_str}")
                text_x = page_width - text_width - 40

                # Draw the text on the right-hand side
                canvas.drawString(text_x, A4[1] - 20, f"SWCM Generated Report {current_datetime_str}")

                # Logo is now stored database side as apprunner does not support local dir calls
                conn = establish_connection()
                query = "SELECT image_data FROM images WHERE id = 1"
                df = pd.read_sql_query(query, conn)
                conn.close()

                # Read the image data from the row
                image_data = df['image_data'][0]

                # Open the image using PIL
                image = PILImage.open(io.BytesIO(image_data))

                # Define the size and position of the image on the canvas
                logo_width = 1.5 * inch
                logo_height = 0.5 * inch
                logo_x = 40  # Adjusted to align with the left-hand side
                logo_y = A4[1] - 40

                # Draw the image onto the canvas
                canvas.drawInlineImage(image, logo_x, logo_y, width=logo_width, height=logo_height)

            def add_page_number(canvas, doc):

                """
                    Function to add the page number to each page of the PDF document.

                    Parameters:
                        canvas (Canvas): The canvas object to draw on.
                        doc (SimpleDocTemplate): The document object representing the PDF.

                    Returns:
                        None
                    """
                current_datetime = datetime.now()

                # Convert the datetime object to a string
                current_datetime_str = current_datetime.strftime("%Y-%m-%d")

                canvas.saveState()
                canvas.setFont("Helvetica", 10)
                canvas.setFillColor(colors.grey)

                page_num = canvas.getPageNumber()
                text = f"Page {page_num}"
                if page_num != 1:
                    canvas.drawString(40, A4[1] - 20, f"SWCM Generated Report {current_datetime_str}")
                canvas.drawRightString(200 * mm, 20 * mm, text)

            def create_paragraph_one():

                """
                    Function to create the first paragraph of the PDF document based on the proforma data of
                    a survey unit. This data is retrieved from the dash aws database proforma table.

                    Returns:
                        str: The text of the first paragraph.
                """

                conn = establish_connection()
                query = f"SELECT * FROM proformas WHERE survey_unit = '{current_survey_unit}'"
                df = pd.read_sql_query(query, conn)

                proforma_text = list(df['proforma'])[0]

                conn.close()

                return proforma_text

            def create_paragraph_two():

                """
                    Function to create the second paragraph of the PDF document based on analysis of the
                    Combined Profile Area (CPA).

                    Returns:
                        str: The text of the second paragraph.
                """

                # try statement when selecting Spring to Spring from map checkbox tend dict returns a list not a dict
                try:
                    if isinstance(trend, list):
                        cal_trend = trend[0]['props']['children']
                    else:
                        cal_trend = trend['props']['children']
                except TypeError as te:
                    pass

                cal_highest = highest_date['props']['children']
                cal_lowest = lowest_date['props']['children']
                cal_highest_val = f"{round(highest_val, 2)}m²"
                cal_lowest_val = f"{round(lowest_val, 2)}m²"

                cal_trend = cal_trend.lower().strip()
                process_state = cal_trend.split(" ")[0]
                rate = cal_trend.split(process_state)[1].strip()
                trend_string = f" {process_state} at a rate of {rate} equating to {percent_change} of the average CPA per year."
                trend_string = trend_string.replace("ˉ", "-")

                state_text = (
                    f"Analysis of the Combined Profile Area (CPA) indicates that {sur_unit_card}  is {trend_string}"
                    f"The highest recorded CPA was recorded on {cal_highest} at {cal_highest_val} and the lowest"
                    f" CPA recorded on {cal_lowest} at {cal_lowest_val}.")

                return state_text

            def add_map_chart():

                """
                    Function to add a map chart to the PDF document.

                    Returns:
                        Image: ReportLab Image object containing the map chart.
                """

                # legend is now stored database side as apprunner does not support local dir calls
                conn = establish_connection()
                query = "SELECT image_data FROM images WHERE id = 2"
                df = pd.read_sql_query(query, conn)
                conn.close()

                # Read the image data from the row
                legend_data = df['image_data'][0]



                # Serialize the figure to JSON
                chart_width, chart_height = A4[1] - 400, A4[0] - 250
                f = map_figure
                map_bytes = pio.to_image(f, format='png')

                # Open the image using PIL
                legend_img = PILImage.open(io.BytesIO(legend_data))
                map_img = PILImage.open(io.BytesIO(map_bytes))

                # Convert both images to RGBA mode to ensure an alpha channel exists
                map_img = map_img.convert("RGBA")
                legend_img = legend_img.convert("RGBA")

                legend_width = 250  # Adjust as needed
                legend_height = 100 # Adjust as needed
                legend_img = legend_img.resize((legend_width, legend_height))

                # Calculate the position to place the legend on top of the map image
                x_offset = 0  # Adjust as needed
                y_offset = 0  # Adjust as needed

                # Composite the legend image on top of the map image
                map_img.paste(legend_img, (x_offset, y_offset), legend_img)

                watermark_text = "          South West\n    Coastal Monitoring"
                font = ImageFont.truetype("arial.ttf", 30)

                # Create a blank image with an alpha channel
                watermark_img = PILImage.new('RGBA', (map_img.width, map_img.height), (14, 14, 14, 0))
                draw = ImageDraw.Draw(watermark_img)

                draw.text((180, 200), watermark_text, fill=(14, 14, 14, 50), font=font)

                # Rotate the watermark text
                rotated_watermark_img = watermark_img.rotate(0, expand=True)


                # Paste the rotated watermark onto the original image
                map_img.paste(rotated_watermark_img, (10, 10), rotated_watermark_img)


                # Convert PIL image to byte array
                with io.BytesIO() as byte_io:
                    map_img.save(byte_io, format='PNG')
                    img_byte_array = byte_io.getvalue()

                # Create a ReportLab Image object
                image = PlatypusImage(io.BytesIO(img_byte_array), width=chart_width, height=chart_height)

                return image

            def add_cpa_chart():

                """
                  Function to add a cpa chart to the PDF document.

                  Returns:
                       Image: ReportLab Image object containing the map chart.
               """

                chart_width, chart_height = A4[1] - 350, A4[0] - 250

                cpa_figure_data = scatter_chart.get("cpa")
                cpa_figure = go.Figure(json.loads(cpa_figure_data), layout=layout)

                # try statement when selecting Spring to Spring from map checkbox tend dict returns a list not a dict
                try:
                    if isinstance(trend, list):
                        cal_trend = trend[0]['props']['children']
                    else:
                        cal_trend = trend['props']['children']
                except TypeError as te:
                    pass

                cal_trend = cal_trend.lower().strip()
                process_state = cal_trend.split(" ")[0]
                rate = cal_trend.split(process_state)[1].strip()

                wrapped_title = 'Survey Unit {0} Combined Profile Area Chart<br> Erosion Rate: {1} equating to {2} of the average CPA per year'.format(
                    current_survey_unit, rate, percent_change)

                cpa_figure.update_layout(
                    xaxis=dict(
                        tickfont=dict(color='black'),
                        title=wrapped_title,
                        title_font=dict(color='black', size=12),
                        automargin=True,
                        title_standoff=8
                    ),
                    yaxis=dict(
                        tickfont=dict(color='black'),
                        title_font=dict(color='black'),
                    ),
                    title=''
                )

                # convert fig to image bytes
                img_bytes = pio.to_image(cpa_figure, format='png')
                img = PILImage.open(io.BytesIO(img_bytes))

                watermark_text = "          South West\n    Coastal Monitoring"
                font = ImageFont.truetype("arial.ttf", 30)

                # Create a blank image with an alpha channel
                watermark_img = PILImage.new('RGBA', (img.width, img.height), (14, 14, 14, 0))
                draw = ImageDraw.Draw(watermark_img)

                draw.text((150, 200), watermark_text, fill=(14, 14, 14, 50), font=font)

                # Rotate the watermark text
                rotated_watermark_img = watermark_img.rotate(0, expand=True)

                # Paste the rotated watermark onto the original image
                img.paste(rotated_watermark_img, (10, 10), rotated_watermark_img)

                # Convert PIL image to byte array
                with io.BytesIO() as byte_io:
                    img.save(byte_io, format='PNG')
                    img_byte_array = byte_io.getvalue()

                # Create a ReportLab Image object
                image = PlatypusImage(io.BytesIO(img_byte_array), width=chart_width, height=chart_height)

                return image

            def add_error_bar_plot():

                """
                    Generate a ReportLab Image object containing an error bar plot.

                    This function creates an error bar plot using Plotly based on the provided error_figure_data.
                    It updates the layout of the plot, including axis labels and title. Then, it converts the Plotly
                    figure to a PNG image byte array using Plotly's to_image function. Next, it converts the PNG image
                    byte array to a PIL image object, and then to a byte array again. Finally, it creates a ReportLab
                    Image object from the byte array with the specified width and height.

                    Returns:
                        reportlab.platypus.Image: A ReportLab Image object containing the error bar plot.
                    """

                chart_width, chart_height = A4[1] - 340, A4[0] - 300
                error_figure_data = error_chart.get("error_plot")
                error_figure = go.Figure(json.loads(error_figure_data))

                error_figure.update_layout(
                    xaxis=dict(
                        tickfont=dict(color='black'),
                        title=f'Box Plot: {current_survey_unit}-{sur_unit_card}',
                        title_font=dict(color='black', size=12),
                        automargin=True,
                        title_standoff=10
                    ),
                    yaxis=dict(
                        tickfont=dict(color='black'),
                        title_font=dict(color='black'),
                    ),
                    title=''
                )

                img_bytes = pio.to_image(error_figure, format='png')
                img = PILImage.open(io.BytesIO(img_bytes))

                watermark_text = "          South West\n    Coastal Monitoring"
                font = ImageFont.truetype("arial.ttf", 30)

                # Create a blank image with an alpha channel
                watermark_img = PILImage.new('RGBA', (img.width, img.height), (14, 14, 14, 0))
                draw = ImageDraw.Draw(watermark_img)

                draw.text((150, 200), watermark_text, fill=(14, 14, 14, 50), font=font)

                # Rotate the watermark text
                rotated_watermark_img = watermark_img.rotate(0, expand=True)

                # Paste the rotated watermark onto the original image
                img.paste(rotated_watermark_img, (10, 10), rotated_watermark_img)

                # Convert the modified PIL image back to byte array
                with io.BytesIO() as byte_io:
                    img.save(byte_io, format='PNG')
                    img_byte_array = byte_io.getvalue()

                # Create a ReportLab Image object
                image = PlatypusImage(io.BytesIO(img_byte_array), width=chart_width, height=chart_height)

                return image

            def add_line_plot():

                """
                    Generate a ReportLab Image object containing a line plot.

                    This function creates a line plot using Plotly based on the provided line_figure_data.
                    It updates the layout  of the plot, including axis labels and title. Then, it converts the Plotly
                    figure to a PNG image byte array using Plotly's to_image function. Next, it converts the PNG image
                    byte array to a PIL image object, and then to a byte array again. Finally, it creates a ReportLab
                    Image object from the byte array with the specified width and height.

                    Returns:
                        reportlab.platypus.Image: A ReportLab Image object containing the line plot.
                """

                chart_width, chart_height = A4[1] - 320, A4[0] - 280
                line_figure_data = line_chart.get("line_plot")
                line_figure = go.Figure(json.loads(line_figure_data))

                line_figure.update_layout(
                    xaxis=dict(
                        tickfont=dict(color='black'),
                        title=f'Cross Sectional Line Plot: {sur_unit_card}-({current_survey_unit})-{selected_profile}',
                        title_font=dict(color='black', size=12),
                        automargin=True,
                        title_standoff=10
                    ),
                    yaxis=dict(
                        tickfont=dict(color='black'),
                        title_font=dict(color='black'),
                    ),
                    title=''
                )
                # Show only the first, second, and last traces in the legend, this may cause a crash!!
                for i, trace in enumerate(line_figure.data):
                    if i not in [0, len(line_figure.data) - 6, len(line_figure.data) - 5, len(line_figure.data) - 4]:
                        trace.showlegend = False

                img_bytes = pio.to_image(line_figure, format='png')
                img = PILImage.open(io.BytesIO(img_bytes))

                watermark_text = "          South West\n    Coastal Monitoring"
                font = ImageFont.truetype("arial.ttf", 30)


                # Create a blank image with an alpha channel
                watermark_img = PILImage.new('RGBA', (img.width, img.height), (14, 14, 14, 0))
                draw = ImageDraw.Draw(watermark_img)

                draw.text((150, 200), watermark_text, fill=(14, 14, 14, 50), font=font)

                # Rotate the watermark text
                rotated_watermark_img = watermark_img.rotate(0, expand=True)

                # Paste the rotated watermark onto the original image
                img.paste(rotated_watermark_img, (10, 10), rotated_watermark_img)

                # Convert PIL image to byte array
                with io.BytesIO() as byte_io:
                    img.save(byte_io, format='PNG')
                    img_byte_array = byte_io.getvalue()

                # Create a ReportLab Image object
                from reportlab.platypus import Image

                image = PlatypusImage(io.BytesIO(img_byte_array), width=chart_width, height=chart_height)

                return image

            # setting up styles to be used in the report
            styles = getSampleStyleSheet()
            style = styles["Normal"]
            centered_style = styles['Title']
            header_style = ParagraphStyle(name='HeaderStyle', parent=style)
            header_style.fontName = 'Helvetica-Bold'
            wrapped_style = ParagraphStyle(name='WrappedStyle', parent=style, alignment=4)
            italic_style = ParagraphStyle(
                name='Italic',
                fontName='Helvetica-Oblique',  # Use Helvetica-Oblique for italic style
                fontSize=10,
                textColor='grey',
                italic=True,  # Set italic to True
                alignment=1
            )

            # spacers added space between lines
            spacer1 = Spacer(1, 20)
            spacer2 = Spacer(1, 10)

            # Extract the date string from the data structure
            highest_date_string = highest_date['props']['children'].split('-')[0]
            lowest_date_string = "2007"

            # the captions used in the figures and tables
            figure_captions = [
                f"Figure 1 - The Combined Profile Area (CPA) for survey unit {current_survey_unit}, including every spring (red), summer (yellow) and autumn (green) survey completed between {lowest_date_string} and {highest_date_string}.",
                f"Figure 2 - Box Plot of the Cross Sectional area of each interim profile, comparing the current area of the profile (red dot), with the maximum and minimum values 2007 and {highest_date_string}",
                f"Figure 3 - Cross Sectional area of interim profile {selected_profile},comparing the values recorded during each interim survey between 2007 and {highest_date_string}",
                f"Table 1 - Cross Sectional are change in m² and percentage comparing spring interim to spring interim ({csa_table_headers.get('spr_spr')}) and baseline to lastest spring interim 9{csa_table_headers.get('baseline_spr')}) "]

            # creating report paragraph objects
            title_paragraph = Paragraph(f"<b>{current_survey_unit}-{sur_unit_card}</b>", centered_style)
            proforma_header = Paragraph("Background", header_style)
            proforma_paragraph = Paragraph(create_paragraph_one(), wrapped_style)
            state_header = Paragraph("Survey Unit Analysis", header_style)
            state_paragraph = Paragraph(create_paragraph_two(), wrapped_style)

            # changing the tables headings and data to exctract based on if autumns present (Scilly) issue.
            check_if_autumns_used = [d for d in spr_to_spr_table if 'Autumn' in str(d.keys())]

            if len(check_if_autumns_used) == 0:

                # CREATE THE CSA TABLE
                table_data = [["Profile", "Spring to Spring Diff (m²)", "Spring to Spring % Change",
                               "Baseline to Spring Diff (m²)", "Baseline to Spring % Change"]]

                for spring_row, baseline_row in zip(spr_to_spr_table, spr_to_baseline_table):
                    profile = spring_row['Profile']
                    spring_diff = spring_row.get('Spring to Spring Diff (m²)', '')
                    spring_percent_change = spring_row.get('Spring to Spring % Change', '')
                    baseline_diff = baseline_row.get('Baseline to Spring Diff (m²)', '')
                    baseline_percent_change = baseline_row.get('Baseline to Spring % Change', '')
                    table_data.append(
                        [profile, spring_diff, spring_percent_change, baseline_diff, baseline_percent_change])
            else:

                # CREATE THE CSA TABLE
                table_data = [["Profile", "Autumn to Autumn Diff (m²)", "Autumn to Autumn % Change",
                               "Baseline to Autumn Diff (m²)", "Baseline to Autumn % Change"]]

                for spring_row, baseline_row in zip(spr_to_spr_table, spr_to_baseline_table):
                    profile = spring_row['Profile']
                    spring_diff = spring_row.get('Autumn to Autumn Diff (m²)', '')
                    spring_percent_change = spring_row.get('Autumn to Autumn % Change', '')
                    baseline_diff = baseline_row.get('Baseline to Autumn Diff (m²)', '')
                    baseline_percent_change = baseline_row.get('Baseline to Autumn % Change', '')
                    table_data.append(
                        [profile, spring_diff, spring_percent_change, baseline_diff, baseline_percent_change])

            spanned_row = ['', csa_table_headers.get('spr_spr'), csa_table_headers.get('spr_spr'),
                           csa_table_headers.get('baseline_spr'), csa_table_headers.get('baseline_spr')]
            table_data.insert(0, spanned_row)

            # Define table style
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                                ('SPAN', (1, 0), (2, 0)),
                                ('SPAN', (3, 0), (4, 0)),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, 0), 8),  # Font size for the first row
                                ('FONTSIZE', (0, 1), (-1, 1), 7),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
                                ('GRID', (0, 0), (-1, -1), 1, colors.darkgray),

                                ])

            # Define column widths
            column_widths = [50, 110, 110, 115, 115]

            # Create table object
            table = Table(table_data, colWidths=column_widths)
            table.setStyle(style)

            # Apply conditional formatting to the second column
            for row_index, row in enumerate(table_data[1:], start=1):  # Skip header row
                for col_index, cell_value in enumerate(row[1:], start=1):  # Iterate over columns 2, 3, 4, and 5
                    if isinstance(cell_value, (int, float)):
                        if cell_value > 30:
                            bg_color = 'rgb(0, 57, 128)'
                        elif 15 <= cell_value <= 30:
                            bg_color = 'rgb(0, 103, 230)'
                        elif 5 <= cell_value <= 15:
                            bg_color = '#00ACE6'
                        elif -5 <= cell_value <= 5:
                            bg_color = colors.grey
                        elif -15 <= cell_value <= -5:
                            bg_color = '#FF9999'
                        elif -30 <= cell_value <= -15:
                            bg_color = '#FF6666'
                        elif cell_value < -30:
                            bg_color = '#FF0000'
                        else:
                            bg_color = None

                        if bg_color:
                            table.setStyle(TableStyle([
                                ('BACKGROUND', (col_index, row_index), (col_index, row_index), bg_color),
                                ('TEXTCOLOR', (col_index, row_index), (col_index, row_index), colors.white)
                            ]))

            chart_flowable_cpa = add_cpa_chart()
            cpa_chart_title = Paragraph(figure_captions[0], italic_style)

            # add map
            map_chart_flowable = add_map_chart()



            # add csa table caption
            csa_table_caption = Paragraph(figure_captions[3], italic_style)

            content_first_page = [title_paragraph, spacer1, proforma_header, spacer2, proforma_paragraph, spacer1,
                                  map_chart_flowable, spacer1, csa_table_caption, spacer2, table, PageBreak(),
                                  state_header, spacer2, state_paragraph, spacer1, chart_flowable_cpa, spacer1,
                                  cpa_chart_title, PageBreak()]

            # Create a flowable object for the error bar chart and add title underneath
            chart_flowable_error = add_error_bar_plot()
            content_first_page.append(chart_flowable_error)
            content_first_page.append(spacer1)
            error_chart_title = Paragraph(figure_captions[1], italic_style)
            content_first_page.append(error_chart_title)

            # Create a flowable object for the line  chart and add title underneath
            line_chart_flowable = add_line_plot()
            content_first_page.append(line_chart_flowable)
            line_chart_title = Paragraph(figure_captions[2], italic_style)
            content_first_page.append(line_chart_title)

            # add new page
            content_first_page.append(PageBreak())

            # building the doc from the content list
            doc.build(
                content_first_page,
                onFirstPage=lambda canvas, doc:  (header(canvas, doc),
                                                 add_page_number(canvas, doc)),
                onLaterPages=lambda canvas, doc: (
                                                 add_page_number(canvas, doc)),
            )

            # grab the first item in the buffer
            buffer.seek(0)
            return buffer.getvalue()

        pdf_bytes = to_pdf()

    current_datetime = datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%d")

    report_name  = f"SWCM_Generated_Report_{current_survey_unit}_{current_datetime_str}.pdf"
    return dcc.send_bytes(pdf_bytes, filename=report_name), {'is_loading': True}


# MODALS
@callback(
    Output("overall_trend_info_model", "is_open"),
    [Input("overall_trend_open_info", "n_clicks"), Input("overall_trend_info_close", "n_clicks")],
    [State("overall_trend_info_model", "is_open")],
)
def toggle_modal(n1, n2, is_open):

    """
       Toggle the state of the overall_trend_info modal based on click events.

       This function toggles the state of the modal between open and closed based on click events.
       It takes two input parameters: n1 and n2, which represent the number of clicks on the open and
       close buttons respectively. The is_open parameter represents the current state of the modal.
       If either n1 or n2 is truthy (indicating a click event), it returns the opposite of the current
       state (toggling it). Otherwise, it returns the current state unchanged.

       Parameters:
           n1 (int or None): Number of clicks on the open button.
           n2 (int or None): Number of clicks on the close button.
           is_open (bool): Current state of the modal (True for open, False for closed).

       Returns:
           bool: Updated state of the modal after toggling.
       """
    if n1 or n2:
        return not is_open
    return is_open


@callback(
    Output("percent_change_info_model", "is_open"),
    [Input("percent_change_open_info", "n_clicks"), Input("percent_change_info_close", "n_clicks")],
    [State("percent_change_info_model", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    """
           Toggle the state of the percent_change_info_model based on click events.

           This function toggles the state of the modal between open and closed based on click events.
           It takes two input parameters: n1 and n2, which represent the number of clicks on the open and
           close buttons respectively. The is_open parameter represents the current state of the modal.
           If either n1 or n2 is truthy (indicating a click event), it returns the opposite of the current
           state (toggling it). Otherwise, it returns the current state unchanged.

           Parameters:
               n1 (int or None): Number of clicks on the open button.
               n2 (int or None): Number of clicks on the close button.
               is_open (bool): Current state of the modal (True for open, False for closed).

           Returns:
               bool: Updated state of the modal after toggling.
    """


    if n1 or n2:
        return not is_open
    return is_open
