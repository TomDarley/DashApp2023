import dash
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
import io
import base64

layout = html.Div([
    dcc.Store(id='line_chart'),


    dcc.Graph(id="line_plot", style={"width": "100%", "height": "50vh", 'margin-left': '0px',}),
    dbc.Button(
            [html.Span(className="bi bi-info-circle-fill")],
            size="md",
            id="line_open_info",
            n_clicks=0,
            className="mr-3",
            style={'position': 'absolute', 'bottom': '1%', 'left': '8px'},
        ),

    dbc.Button(
        [html.Span(className="fa-solid fa-expand")],
        size="md",
        id="line_open_full",
        n_clicks=0,
        className="mr-3",
        style={'position': 'absolute', 'bottom': '1%', 'right': '8px'},
    ),



    dbc.Button(
            [html.Span(className="bi bi-badge-3d")],
            size="md",
            id="3D_plot",
            n_clicks=0,
            className="mr-3",
            style={'position': 'absolute', 'top': '1%', 'left': '60px'},
        ),

    dbc.Button(
            [html.Span(className="bi bi-badge-sd")],
            size="md",
            id="2D_plot",
            n_clicks=0,
            className="mr-3",
            style={'position': 'absolute', 'top': '1%', 'left': '8px'},
        ),




    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Cross Sectional Line Plot")),
                dbc.ModalBody("This is a nice chart!"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="line_info_close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="line_info_model",
            is_open=False,
            fullscreen=True,
        ),
    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Cross Sectional Line Plot")),
                dbc.ModalBody(dcc.Graph(id="line_plot_model", style={'height': '100vh'})),## might not work
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="line_full_close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_line_plot",
            is_open=False,
            fullscreen=True,
    ),
                       
    ],style={'position': 'relative', 'margin-bottom': '10px','margin-top': '20px','margin-right': '0px'},
)


@callback(
    Output("line_plot", "figure"),
    Output("line_plot_model", "figure"),
    Output('line_chart', "data"),


    Input('survey-unit-dropdown', 'value'),
    Input('survey-line-dropdown', 'value'),
    Input('3D_plot', 'n_clicks'),
    Input('2D_plot', 'n_clicks'),


    prevent_initial_call=False,
    allow_duplicate=True)

def make_line_plot(selected_sur_unit, selected_profile, n_clicks_3d, n_clicks_2d):

    # check if a chart mode button has been selected, use it to render the correct chart mode
    trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(trigger)
    if trigger == '3D_plot.n_clicks':
        selection = '3D'
    elif trigger == '2D_ploy_n_clicks':
        selection = '2D'
    else:
        selection = '2D'


    # All shapefile loaded into the database should not be promoted to multi
    engine = create_engine("postgresql://postgres:Plymouth_C0@localhost:5432/Dash_DB")
    # Connect to the database using the engine
    conn = engine.connect()

    # Load topo data from DB
    topo_query = f"SELECT * FROM topo_data WHERE survey_unit = '{selected_sur_unit}' AND profile = '{selected_profile}'"  # Modify this query according to your table
    topo_df = pd.read_sql_query(topo_query, conn)
    topo_df =topo_df.sort_values(by='chainage')

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



    #dummy_y= topo_df['date'].

    if selection == '3D':

        # create 3D plot
        surface_elevation = []
        for x in range(len(topo_df['chainage'])):
            surface_elevation.append(master_profile_elevation)

        fig = px.line_3d(topo_df, x= 'chainage', y='date', z= 'elevation_od',color='date')



        fig.add_trace(
            go.Surface(x=master_profile_chainage,y =topo_df['date'] , z= surface_elevation,showlegend=False,
                       name='Master Profile', colorscale='Fall')

        )

        fig.update_layout(
            legend=dict(
                orientation='h',  # Horizontal orientation
                yanchor='top',  # Anchor to the top of the chart
                y=1.05,  # Adjust the vertical position as needed
                xanchor='left',  # Anchor to the left side of the chart
                x=0.01  # Adjust the horizontal position as needed
            )
        )
    else:

        # Create a 2D line plot
        fig = px.line(topo_df, x='chainage', y='elevation_od', color='date',
                      color_discrete_sequence=px.colors.qualitative.D3, template="seaborn", )

        fig.add_trace(
            go.Scatter(x=master_profile_chainage, y=master_profile_elevation,
                       line=dict(color='red', width=5, dash='dash'),
                       name='Master Profile')
        )

    # Customize x and y axis fonts and sizes
    fig.update_xaxes(
        title_text='Chainage (m)',
        title_font=dict(size=15, family='Helvetica', color = 'blue'),  # Customize font size and family
        tickfont=dict(size=15, family='Helvetica', color ='blue')  # Customize tick font size and family
    )

    fig.update_yaxes(
        title_text='Elevation (m)',
        title_font=dict(size=15, family='Helvetica', color = 'blue'),  # Customize font size and family
        tickfont=dict(size=15, family='Helvetica', color ='blue')  # Customize tick font size and family
    )

    # Customize the legend font and size
    fig.update_layout(
        legend=dict(
            title_font=dict(size=12, family='Helvetica'),  # Customize font size and family
            title_text='',  # Remove legend title
            font=dict(size=12, family='Helvetica')  # Customize font size and family for legend labels
        ),
        legend_traceorder='reversed',
        legend_title_text=f''
    )

    # Add a title to the plot
    fig.update_layout(title=f'{selected_profile}', title_font=dict(size=12, family='Helvetica'),title_x=0.5)

    # Serialize the figure to JSON
    serialized_fig = fig.to_json()

    # Update the 'cpa' key in the store's data with the serialized figure
    chart_data = {"line_plot": serialized_fig}



    return fig, fig, chart_data


@callback(
    Output("line_info_model", "is_open"),
    [Input("line_open_info", "n_clicks"), Input("line_info_close", "n_clicks")],
    [State("line_info_model", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@callback(
    Output("modal_line_plot", "is_open"),
    Output("line_open_full", "n_clicks"),
    Input("line_open_full", "n_clicks"),
    Input("line_full_close", "n_clicks"),
    Input("line_plot", "relayoutData")
)
def toggle_modal_chart(n1, n2, relayoutData):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if "open" in changed_id:
        return True, 0
    elif "close" in changed_id:
        return False, 0
    return False, 0








