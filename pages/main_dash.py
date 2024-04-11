import dash
from dash import html, callback, Input, Output, State
from apps import scatter_plot
from apps import error_bar_plot
from apps import map_box_3
from apps import profile_line_plot
from apps import csa_table
import dash_bootstrap_components as dbc
from dash import dcc
import json
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Spacer
from reportlab.lib.units import inch
import io
import plotly.io as pio
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from sqlalchemy import create_engine
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import StringIO
from reportlab.platypus import PageBreak
import json
from PIL import Image as PILImage
from datetime import datetime
dash.register_page(__name__, path="/main_dash")



# define the layout of the main page
layout = html.Div(
    [  # Add the image

        dcc.Store(
            id="generated_charts",
            data={"cpa": None, "line_plot": None, "error_plot": None},
        ),

        dcc.Download(id="download"),
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
                                                        "label": "6eB3-2 & 6eB3-3  -  Green Bay",
                                                        "value": "6eB3-2 & 6eB3-3",
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
                                                    "margin-bottom": "5px",
                                                    "font-weight": 'bold'
                                                },
                                            ),
                                            #dcc.Checklist(
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

                                            #),
                                            dbc.Button(
                                                "Generate Report",
                                                id="download-charts-button",
                                                n_clicks=0,
                                                size="sm",
                                                style={"border-radius": "10px"},
                                                className='mr-3',

                                            ),
                                        ]
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
                            #duration=4000,
                            color="danger",
                            style={'position': 'absolute', 'top': '0', 'left': '0', 'right': '0', 'zIndex': 1000}
                        ),

                        profile_line_plot.layout,






                             ],style={'position': 'relative'}),

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
    ],
)


@callback(

    Output("survey_unit_card", "children"),

    Input("survey-unit-dropdown", "value"),
    State("survey-unit-dropdown", "options"),

)
def update_survey_unit_card(current_sur_unit, current_sur_unit_state):
    """Callback populates the survey unit CPA card with the current selected survey unit"""

    if current_sur_unit:
        label = [
            x["label"] for x in current_sur_unit_state if x["value"] == current_sur_unit
        ]

        label = label[0].split(" -")[1].strip()

        return label


@callback(
    Output("trend_card", "children"),

    Input("change_rate", "data"),
    Input("survey-points-change-values", 'data'),
    Input("change_range_radio_button", 'value'),


)
def update_trend_card(trend,survey_points_change_values,change_range_radio_button, ):
    """Callback grabs the trend data from the change rate store found in the scatter plot page.
    Formats the output string"""

    # Load JSON into DataFrame
    with StringIO(survey_points_change_values) as json_data:
        change_values = pd.read_json(json_data)

    classification = list(change_values['features'])[0]
    classification_string = classification['properties']['classification']

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
    if change_range_radio_button != "spr-spr":
        color_to_use = color_mapping[classification_string]


    if trend:
        if "Accretion Rate" in trend:
            value = trend.split(":")[-1]
            comment = f" Accreting {value}"
            if change_range_radio_button != "spr-spr":

                return html.Span(f"{comment}", style={"color": color_to_use})
            else:
                return html.Span(f"{comment}"),


        elif "Erosion Rate" in trend:
            value = trend.split(":")[-1]
            comment = f" Eroding {value}"
            if change_range_radio_button != "spr-spr":

                return html.Span(f"{comment}", style={"color": color_to_use})
            else:
                return html.Span(f"{comment}"),



    else:
        return f"{trend}"


## Add card for spr to spr percent change or baseline to baselinw percent change

@callback(
    Output("trend_card1", "children"),
    Input("survey-points-change-values", 'data'),#
    State('change_range_radio_button', 'value')
)
def update_percent_change_card(change_value, change_range_radio_button):
    """Callback updates the percent change card, based on survey unit selected CPA change between either
       the baseline to spr or spr to spr selection"""
    # Load JSON into DataFrame
    with StringIO(change_value) as json_data:
        change_values = pd.read_json(json_data)

    classification = list(change_values['features'])[0]
    classification_string = classification['properties']['classification']
    percent_change = round(classification['properties']['difference'],2)

    comment = None

    print(classification)
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
    comment = "Error"
    if classification_string in ['High Erosion','Mild Erosion','Low Erosion' ]:
        value = percent_change
        if change_range_radio_button == 'base-spr':
            comment = f"{value} %"
        else:
            comment = f"{value} %"

        return html.Span(f"{comment}", style={"color": color_to_use})
    elif classification_string in ['High Accretion','Mild Accretion','Low Accretion' ]:
        value = percent_change
        if change_range_radio_button == 'base-spr':
            comment = f"+ {value} %"
        else:
            comment = f"+ {value} %"

        return html.Span(f"{comment}", style={"color": color_to_use})
    elif classification_string == 'No Change':
        value = percent_change
        if change_range_radio_button == 'base-spr':
            comment = f"Baseline to Latest Spring +/- {value} %"
        else:
            comment = f"Spring to Latest Spring + +/- {value} %"

        comment =  f" +/- {value} %"

    return comment



@callback(
    Output("lowest_card", "children"),
    Input("lowest_recorded_value", "data"),
    Input("lowest_recorded_year", "data"),
)
def update_lowest_cpa_card(lowest_data, lowest_year):
    """Callback updates the lowest cpa card. It grabs the data from the stores in the scatter plot page"""

    if lowest_data and lowest_year:
        comment = f"{lowest_data} "
        return html.Span(f"{comment}", style={"color": "red"})


@callback(
    Output("highest_card", "children"),
    Input("highest_recorded_value", "data"),
    Input("highest_recorded_year", "data"),
)
def update_highest_cpa_card(highest_data, highest_year):
    """Callback updates the highest cpa card. It grabs the data from the stores in the scatter plot page"""
    if highest_data and highest_year:
        comment = f"{highest_data} "
        return html.Span(f"{comment}", style={"color": "green"})


@callback(

    Output("download", "data"),
    Input("download-charts-button", "n_clicks"),
    #State("download-check-list", "value"),
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
    State('csa_header_store',"data"),
    State('percent_change', "data"),

    allow_duplicate=True,
    prevent_initial_call=True,
)
def get_selected_charts(
        n_clicks, scatter_chart, error_chart, line_chart,
        sur_unit_card, current_survey_unit, trend, highest_date, lowest_date, highest_val, lowest_val, spr_to_spr_table,spr_to_baseline_table, csa_table_headers, percent_change
):
    """Function controls the logic behind which charts are to be downloaded using the download checklist"""

    if n_clicks is None:
        raise PreventUpdate

    if n_clicks is None:
        return dash.no_update
    else:

        def to_pdf():

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)

            def header(canvas, doc):
                # Get the current date and time
                current_datetime = datetime.now()

                # Convert the datetime object to a string
                current_datetime_str = current_datetime.strftime("%Y-%m-%d")

                canvas.saveState()
                canvas.setFont("Helvetica", 10)
                canvas.setFillColor(colors.grey)
                canvas.drawString(40, A4[1] - 20, f"SWCM Generated Report {current_datetime_str}")
                logo_width = 1.5 * inch
                logo_height = 0.5 * inch
                logo_x = A4[0] - inch - logo_width
                logo_y = A4[1] - 40
                canvas.drawImage(r"assets\Full-Logo (white sky).png", logo_x,
                                 logo_y, width=logo_width, height=logo_height, mask="auto")
                canvas.restoreState()

            def footer(canvas, doc):
                canvas.saveState()
                canvas.setFont("Helvetica", 9)
                canvas.drawString(40, 20, f"Page {doc.page}")
                canvas.restoreState()

            def create_paragraph_one():
                engine = create_engine(
                    "postgresql://postgres:Plymouth_C0@swcm-dashboard.crh7kxty9yzh.eu-west-2.rds.amazonaws.com:5432/postgres")
                conn = engine.connect()

                survey_unit = current_survey_unit
                query = f"SELECT * FROM proformas WHERE survey_unit = '{current_survey_unit}'"
                df = pd.read_sql_query(query, conn)

                proforma_text = list(df['proforma'])[0]

                return proforma_text

            def create_paragraph_two():
                cal_trend = trend['props']['children']
                cal_highest = highest_date['props']['children']
                cal_lowest = lowest_date['props']['children']
                cal_highest_val = f"{round(highest_val, 2)}m²"
                cal_lowest_val = f"{round(lowest_val, 2)}m²"

                cal_trend = cal_trend.lower().strip()
                process_state = cal_trend.split(" ")[0]
                rate = cal_trend.split(process_state)[1].strip()
                trend_string = f" {process_state} at a rate of {rate} equating to {percent_change} of the average CPA per year."
                state_text = (
                    f"Analysis of the Combined Profile Area (CPA) indicates that {sur_unit_card}  is {trend_string}"
                    f"The highest recorded CPA was recorded on {cal_highest} at {cal_highest_val} and the lowest"
                    f" CPA recorded on {cal_lowest} at {cal_lowest_val}.")

                return state_text

            def add_CPA_chart(canvas, doc):
                chart_width, chart_height = A4[1] - 350, A4[0] - 250

                cpa_figure_data = scatter_chart.get("cpa")
                cpa_figure = go.Figure(json.loads(cpa_figure_data), layout=layout)

                cal_trend = trend['props']['children']
                cal_trend = cal_trend.lower().strip()
                process_state = cal_trend.split(" ")[0]
                rate = cal_trend.split(process_state)[1].strip()

                cpa_figure.update_layout(
                    xaxis=dict(
                        tickfont=dict(color='black'),
                        title=f'{current_survey_unit} Combined Profile Area Chart\nErosion Rate:{rate} equating to {percent_change} of the average CPA per year',
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

                img_bytes = pio.to_image(cpa_figure, format='png')
                img_io = io.BytesIO(img_bytes)
                img_reader = ImageReader(img_io)
                canvas.drawImage(img_reader, 70, 200, width=chart_width, height=chart_height)

            def add_error_bar_plot():
                chart_width, chart_height = A4[1] - 350, A4[0] - 250
                error_figure_data = error_chart.get("error_plot")
                error_figure = go.Figure(json.loads(error_figure_data))

                error_figure.update_layout(
                    xaxis=dict(
                        tickfont=dict(color='black'),
                        title=f'exgxgfxgfxgfxgfxgfx',
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

                img_bytes = pio.to_image(error_figure, format='png')
                img = PILImage.open(io.BytesIO(img_bytes))

                # Convert PIL image to byte array
                with io.BytesIO() as byte_io:
                    img.save(byte_io, format='PNG')
                    img_byte_array = byte_io.getvalue()

                # Create a ReportLab Image object
                from reportlab.platypus import Image
                chart_flowable = Image(io.BytesIO(img_byte_array), width=chart_width, height=chart_height)

                return chart_flowable

            def add_line_plot():

                """Request to add a generator here that makes all the charts for a survey unit?"""

                chart_width, chart_height = A4[1] - 350, A4[0] - 280
                line_figure_data = line_chart.get("line_plot")
                line_figure = go.Figure(json.loads(line_figure_data))

                line_figure.update_layout(
                    xaxis=dict(
                        tickfont=dict(color='black'),
                        title=f'exgxgfxgfxgfxgfxgfx',
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

                img_bytes = pio.to_image(line_figure, format='png')
                img = PILImage.open(io.BytesIO(img_bytes))

                # Convert PIL image to byte array
                with io.BytesIO() as byte_io:
                    img.save(byte_io, format='PNG')
                    img_byte_array = byte_io.getvalue()

                # Create a ReportLab Image object
                from reportlab.platypus import Image
                chart_flowable1 = Image(io.BytesIO(img_byte_array), width=chart_width, height=chart_height)

                return chart_flowable1

            styles = getSampleStyleSheet()
            style = styles["Normal"]
            centered_style = styles['Title']

            header_style = ParagraphStyle(name='HeaderStyle', parent=style)
            header_style.fontName = 'Helvetica-Bold'

            wrapped_style = ParagraphStyle(name='WrappedStyle', parent=style, wordWrap='CJK')

            spacer1 = Spacer(1, 20)
            spacer2 = Spacer(1, 10)

            title_paragraph = Paragraph(f"<b>{current_survey_unit}-{sur_unit_card}</b>", centered_style)
            proforma_header = Paragraph("Background", header_style)
            proforma_paragraph = Paragraph(create_paragraph_one(), wrapped_style)
            state_header = Paragraph("Survey Unit Analysis", header_style)
            state_paragraph = Paragraph(create_paragraph_two(), wrapped_style)

            content_first_page =  [title_paragraph, spacer1, proforma_header, spacer2, proforma_paragraph, spacer1, state_header, spacer2,
                                    state_paragraph, spacer1]

            content_first_page.append(PageBreak())
            # Create a flowable object for the chart
            chart_flowable = add_error_bar_plot()
            content_first_page.append(chart_flowable)
            line_chart_flowable = add_line_plot()
            content_first_page.append(line_chart_flowable)




            doc.build(
                content_first_page,
                onFirstPage=lambda canvas, doc: (
                    header(canvas, doc), add_CPA_chart(canvas, doc), footer(canvas, doc)),
                onLaterPages=lambda canvas, doc: (
                    footer(canvas, doc)  # Define the content for subsequent pages
                ))


            buffer.seek(0)
            return buffer.getvalue()

        pdf_bytes = to_pdf()


        # Save the subplot as an image
        # img_bytes = subplot.to_image(format="png")

    return dcc.send_bytes(pdf_bytes, filename='test.pdf')
    # return subplot, dcc.send_bytes(img_bytes, filename="SWCM_Chart_Selection.png")
