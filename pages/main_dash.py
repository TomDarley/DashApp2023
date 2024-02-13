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
import io
import plotly.io as pio
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from sqlalchemy import create_engine
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import base64

dash.register_page(__name__, path="/main_dash")

image_path = r"media/map_legend.PNG"
with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

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
                                                options=[{'label': "6a01613", 'value': "6a01613"},
                                                         {'label': "6a01614", 'value': "6a01614"},
                                                         {'label': "6a01615", 'value': "6a01615"},
                                                         {'label': "6a01616", 'value': "6a01616"},
                                                         {'label': "6a01617", 'value': "6a01617"},
                                                         {'label': "6a01618", 'value': "6a01618"},
                                                         {'label': "6a01619", 'value': "6a01619"},
                                                         {'label': "6a01620", 'value': "6a01620"},
                                                         {'label': "6a01621", 'value': "6a01621"},
                                                         {'label': "6a01622", 'value': "6a01622"},
                                                         {'label': "6a01623", 'value': "6a01623"},
                                                         {'label': "6a01624", 'value': "6a01624"}],
                                                value="6a01613",
                                                id="survey-line-dropdown",

                                            ),
                                            dcc.Dropdown(
                                                options=[

                                                    {
                                                        "label": "Interim Surveys",
                                                        "value": "Interim",
                                                    },
                                                    {
                                                        "label": "Baseline Surveys",
                                                        "value": "Baseline",
                                                    },
{
                                                        "label": "Post Storm Surveys",
                                                        "value": "Post Storm",
                                                    },
                                                ],
                                                value="Interim",
                                                id="survey-type-dropdown",
                                                multi=True

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
                                                "Trend:",
                                                className="card-title",
                                                style={
                                                    "color": "blue",
                                                    "margin-bottom": "5px",
                                                    "font-weight": 'bold'

                                                },
                                            ),
                                            html.Div("----", id="trend_card"),
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
                                            dcc.Checklist(
                                                id="download-check-list",
                                                options=[
                                                    {
                                                        "label": " CPA Plot ",
                                                        "value": "cpa",
                                                    },
                                                    {
                                                        "label": " CSL Plot ",
                                                        "value": "line_plot",
                                                    },
                                                    {
                                                        "label": " Box Plot",
                                                        "value": "box_plot",
                                                    },
                                                ],
                                                value=['cpa','line_plot','box_plot'],
                                                labelStyle={"margin-right": "10px"},
                                                style={"color": "#045F36", "font-weight": "bold", "font-size": "15px"},
                                                # inline=True,

                                            ),
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
)
def update_trend_card(trend):
    """Callback grabs the trend data from the change rate store found in the scatter plot page.
    Formats the output string"""

    if trend:
        if "Accretion Rate" in trend:
            value = trend.split(":")[-1]
            comment = f" Accreting {value}"
            return html.Span(f"{comment}", style={"color": "green"})
        elif "Erosion Rate" in trend:
            value = trend.split(":")[-1]
            comment = f" Eroding {value}"
            return html.Span(f"{comment}", style={"color": "red"})
    else:
        return f"{trend}"


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
    State("download-check-list", "value"),
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

    allow_duplicate=True,
    prevent_initial_call=True,
)
def get_selected_charts(
        n_clicks, chart_selection, scatter_chart, error_chart, line_chart,
        sur_unit_card, current_survey_unit, trend, highest_date, lowest_date, highest_val, lowest_val, spr_to_spr_table,spr_to_baseline_table, csa_table_headers
):
    """Function controls the logic behind which charts are to be downloaded using the download checklist"""

    if n_clicks is None:
        raise PreventUpdate

    if n_clicks is None:
        return dash.no_update
    else:

        def to_pdf():

            # Get the proforma text from the database
            engine = create_engine(
                "postgresql://postgres:Plymouth_C0@swcm-dashboard.crh7kxty9yzh.eu-west-2.rds.amazonaws.com:5432/postgres")
            conn = engine.connect()

            survey_unit = current_survey_unit
            query = f"SELECT * FROM proformas WHERE survey_unit = '{current_survey_unit}'"
            df = pd.read_sql_query(query, conn)

            proforma_text = list(df['proforma'])[0]

            # Generate the current state paragraph trend, highest, lowest
            cal_trend = trend['props']['children']
            cal_highest = highest_date['props']['children']
            cal_lowest = lowest_date['props']['children']
            cal_highest_val = f"{round(highest_val, 2)} (m²)"
            cal_lowest_val = f"{round(lowest_val, 2)} (m²)"

            cal_trend = cal_trend.lower()
            state_text = f"Analysis of the Combined Profile Area (CPA) indicates that {survey_unit} is {cal_trend}." \
                         f"The highest recorded CPA was recorded on {cal_highest} at {cal_highest_val} and the lowest" \
                         f" CPA recorded on {cal_lowest} at {cal_lowest_val}"

            # Create a stylesheet for text wrapping
            styles = getSampleStyleSheet()
            style = styles["Normal"]

            # Set the desired width for text wrapping
            text_width = A4[0] - 100  # Adjust as needed this higher number makes the right margin larger

            # Create a PDF document
            buffer = io.BytesIO()  # in ram storage

            # Create a canvas
            c = canvas.Canvas(buffer, pagesize=portrait(A4))

            width, height = A4[1] - 300, A4[0] - 250  # Adjust these values as needed

            # Create a ParagraphStyle for text wrapping
            wrapped_style = ParagraphStyle(name='WrappedStyle', parent=style, wordWrap='CJK')

            # Create a flowable paragraph
            proforma_paragraph = Paragraph(proforma_text, wrapped_style)
            proforma_paragraph2 = Paragraph(state_text, wrapped_style)

            # Add the Title
            c.drawCentredString(A4[0] / 2, 780, f"{survey_unit}-{sur_unit_card}!")

            # Add the proforma paragraph to the canvas
            proforma_paragraph.wrapOn(c, text_width, A4[1])
            proforma_paragraph.drawOn(c, 50, 680)

            # Add the stats paragraph
            proforma_paragraph2.wrapOn(c, text_width, A4[1])
            proforma_paragraph2.drawOn(c, 50, 630)

            # logic to define the first chosen plot:
            charts_selected = []
            if "cpa" in chart_selection:
                charts_selected.append('cpa')
            if "line_plot" in chart_selection:
                charts_selected.append('line_plot')
            if "box_plot" in chart_selection:
                charts_selected.append('box_plot')

            for index, item in enumerate(charts_selected):

                if item == "cpa":
                    cpa_figure_data = scatter_chart.get("cpa")
                    cpa_figure = go.Figure(json.loads(cpa_figure_data), layout=layout)
                    img_bytes = pio.to_image(cpa_figure, format='png')
                    img_io = io.BytesIO(img_bytes)
                    img_reader = ImageReader(img_io)
                    c.drawImage(img_reader, 20, 250, width=width, height=height)
                    c.showPage()

                if item == "line_plot":
                    line_figure_data = line_chart.get("line_plot")
                    line_figure = go.Figure(json.loads(line_figure_data))
                    img_bytes = pio.to_image(line_figure, format='png')
                    img_io = io.BytesIO(img_bytes)
                    img_reader = ImageReader(img_io)

                    if index == 0:
                        c.drawImage(img_reader, 20, 250, width=width, height=height, )
                        c.showPage()

                    elif index == 1:
                        c.drawImage(img_reader, 20, 450, width=width, height=height, )
                    else:
                        c.drawImage(img_reader, 20, 50, width=width, height=height, )

                if item == "box_plot":
                    error_figure_data = error_chart.get("error_plot")
                    error_figure = go.Figure(json.loads(error_figure_data))
                    img_bytes = pio.to_image(error_figure, format='png')
                    img_io = io.BytesIO(img_bytes)
                    img_reader = ImageReader(img_io)

                    if index == 0:
                        c.drawImage(img_reader, 20, 250, width=width, height=height, )
                        c.showPage()

                    elif index == 1:
                        c.drawImage(img_reader, 20, 450, width=width, height=height, )
                    else:
                        c.drawImage(img_reader, 20, 50, width=width, height=height, )


            # Define column widths (adjust as needed)
            col_widths = [100, 200, 200]

            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ])

            # get the table header information
            spr_spr_header = csa_table_headers.get('spr_spr').replace(" - ", ' to ')
            baseline_spr_header = csa_table_headers.get('baseline_spr').replace(" - ", ' to ')

            width = 800
            height = 100

            dfs = []
            index = [0]
            for data in spr_to_spr_table:
                df = pd.DataFrame(data, index=index)
                dfs.append(df)

            main_df = pd.concat(dfs)
            table_data = [main_df.columns.tolist()] + main_df.values.tolist()

            spr_to_spr_ = Table(table_data,colWidths=col_widths)

            spr_to_spr_.setStyle(style)
            spr_to_spr_.wrapOn(c, width, height)
            c.showPage()
            # Add the Title
            c.drawCentredString(A4[0] / 2, 800, 'CSA Tables')
            c.drawString(50, 750, spr_spr_header)
            spr_to_spr_.drawOn(c, 50, 400)

            dfs = []
            index = [0]
            for data in spr_to_baseline_table:
                df = pd.DataFrame(data, index=index)
                dfs.append(df)

            main_df = pd.concat(dfs)
            table_data = [main_df.columns.tolist()] + main_df.values.tolist()

            spr_to_baseline_ = Table(table_data,colWidths=col_widths)
            spr_to_baseline_.setStyle(style)
            spr_to_baseline_.wrapOn(c, width, height)
            c.showPage()
            c.drawString(50, 750, baseline_spr_header)
            spr_to_baseline_.drawOn(c, 50, 400)


            # Save the PDF file
            c.save()

            buffer.seek(0)
            return buffer.getvalue()

        pdf_bytes = to_pdf()


        # Save the subplot as an image
        # img_bytes = subplot.to_image(format="png")

    return dcc.send_bytes(pdf_bytes, filename='test.pdf')
    # return subplot, dcc.send_bytes(img_bytes, filename="SWCM_Chart_Selection.png")
