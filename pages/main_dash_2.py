import dash
from dash import html, callback, Input, Output, State

# from DashApp2023.apps import survey_unit_dropdown
from DashApp2023.apps import scatter_plot
from DashApp2023.apps import error_bar_plot

# from DashApp2023.apps import leaflet_map
from DashApp2023.apps import mapbox

from DashApp2023.apps import profile_line_plot
from DashApp2023.apps import CSA_Table
import dash_bootstrap_components as dbc
from dash import dcc
from plotly.subplots import make_subplots
import psycopg2
import geopandas as gpd
import json
from dash_extensions.javascript import Namespace
import plotly.graph_objs as go
from datetime import datetime
import io
import base64
from dash.exceptions import PreventUpdate
from base64 import b64encode



# register the page with dash giving url path
dash.register_page(__name__, path="/main_dash2")
layout = html.Div([
    dcc.Store(id='generated_charts',data={"cpa": None, 'line_plot': None, 'error_plot': None} ),
    dcc.Graph(id='hidden-chart', style ={'display': 'none'}),
    dcc.Download(id  ='download'),


    dbc.Row(
        [
            dbc.Col(html.Div([

                dbc.Card([
                    dbc.CardBody([
                        html.H6("Survey Unit:", className="card-title",
                                style={'color': 'blue', 'margin-bottom': '5px', }),
                        html.Div("6aSU12", id='survey_unit_card')

                    ])
                ], style={'margin': '10px', 'border-radius': '10px'}),

                dbc.Card([
                    dbc.CardBody([
                        html.H6("Trend:", className="card-title", style={'color': 'blue', 'margin-bottom': '5px'}),
                        html.Div("----", id='trend_card')

                    ])
                ], style={'margin': '10px', 'border-radius': '10px'}),

                dbc.Card([
                    dbc.CardBody([
                        html.H6("Highest Recorded CPA:", className="card-title",
                                style={'color': 'blue', 'margin-bottom': '5px'}),
                        html.Div("----", id='highest_card')

                    ])
                ], style={'margin': '10px', 'border-radius': '10px'}),

                dbc.Card([
                    dbc.CardBody([
                        html.H6("Lowest Recorded CPA:", className="card-title",
                                style={'color': 'blue', 'margin-bottom': '5px'}),
                        html.Div("----", id='lowest_card')

                    ])
                ], style={'margin': '10px', 'border-radius': '10px'}),

            ]),

                xs={"size": 12, "offset": 0},
                sm={"size": 12, "offset": 0},
                md={"size": 12, "offset": 0},
                lg={"size": 2, "offset": 0},
                xl={"size": 2, "offset": 0},
                xxl={"size": 2, "offset": 0},

                align="start"

            ),

            dbc.Col(html.Div([
                mapbox.layout,

            ],
                style={'margin-top': '10px', 'height': '60vh'}),

                xs={"size": 12, "offset": 0},
                sm={"size": 12, "offset": 0},
                md={"size": 12, "offset": 0},
                lg={"size": 5, "offset": 0},
                xl={"size": 5, "offset": 0},
                xxl={"size": 5, "offset": 0}, ),

            dbc.Col(html.Div(
                scatter_plot.layout,

            ), style={'margin-top': '10px', 'height': '100%', },
                xs={"size": 12, "offset": 0},
                sm={"size": 12, "offset": 0},
                md={"size": 12, "offset": 0},
                lg={"size": 5, "offset": 0},
                xl={"size": 5, "offset": 0},
                xxl={"size": 5, "offset": 0}),
        ],

        align="start",
        style={}

    ),
    dbc.Row(
        [dbc.Col(html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Download Charts:", className="card-title",
                            style={'color': 'blue', 'margin-bottom': '10px', }),


                    dcc.Checklist(id= 'download-check-list',
                        options=[
                            {'label': ' CPA Plot', 'value': 'cpa'},
                            {'label': ' Line Plot', 'value': 'line_plot'},
                            {'label': ' Box Plot', 'value': 'box_plot'}
                        ],
                        value =[]),

                    dbc.Button('Lock Selection',id = 'download-charts-button', n_clicks=0),



                ])
            ], style={'margin': '10px', 'position': 'block', 'border-radius': '10px'}),

        ]), xs={"size": 12, "offset": 0},
            sm={"size": 12, "offset": 0},
            md={"size": 12, "offset": 0},
            lg={"size": 2, "offset": 0},
            xl={"size": 2, "offset": 0},
            xxl={"size": 2, "offset": 0},
            align='start'),
            dbc.Col(html.Div(profile_line_plot.layout), xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0}),

            dbc.Col(html.Div(error_bar_plot.layout), xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0}),

        ],
        align="start", ),
    dbc.Row(
        [dbc.Col(html.Div([]), xs={"size": 12, "offset": 0},
                 sm={"size": 12, "offset": 0},
                 md={"size": 12, "offset": 0},
                 lg={"size": 2, "offset": 0},
                 xl={"size": 2, "offset": 0},
                 xxl={"size": 2, "offset": 0}),
         dbc.Col(html.Div(CSA_Table.layout), xs={"size": 12, "offset": 0},
                 sm={"size": 12, "offset": 0},
                 md={"size": 12, "offset": 0},
                 lg={"size": 10, "offset": 0},
                 xl={"size": 10, "offset": 0},
                 xxl={"size": 10, "offset": 0}),

         ],
        align="start", ),

])


@callback(
    Output("survey_unit_card", "children"),
    Input("survey-unit-dropdown", "value"), )
def update_survey_unit_card(current_sur_unit):
    """Callback populates the survey unit CPA card with the current selected survey unit"""

    if current_sur_unit:
        return current_sur_unit


@callback(
    Output("trend_card", "children"),
    Input("change_rate", "data"), )
def update_trend_card(trend):
    """Callback grabs the trend data from the change rate store found in the scatter plot page.
       Formats the output string"""

    if trend:
        if "Accretion Rate" in trend:
            value = trend.split(':')[-1]
            comment = f" Accreting {value}"
            return html.Span(f"{comment}", style={'color': 'green'})
        elif "Erosion Rate" in trend:
            value = trend.split(':')[-1]
            comment = f" Eroding {value}"
            return html.Span(f"{comment}", style={'color': 'red'})
    else:
        return f"{trend}"


@callback(
    Output("lowest_card", "children"),
    Input("lowest_recorded_value", "data"),
    Input("lowest_recorded_year", "data")
)
def update_lowest_cpa_card(lowest_data, lowest_year):
    """Callback updates the lowest cpa card. It grabs the data from the stores in the scatter plot page"""

    if lowest_data and lowest_year:
        comment = f"{lowest_data} "
        return html.Span(f"{comment}", style={'color': 'red'})


@callback(
    Output("highest_card", "children"),
    Input("highest_recorded_value", "data"),
    Input("highest_recorded_year", "data")
)
def update_highest_cpa_card(highest_data, highest_year):

    """Callback updates the highest cpa card. It grabs the data from the stores in the scatter plot page"""
    if highest_data and highest_year:
        comment = f"{highest_data} "
        return html.Span(f"{comment}", style={'color': 'green'})

@callback(
    Output("hidden-chart", "figure"),
    Output("download", "data"),
    Input('download-charts-button', 'n_clicks'),
    State('download-check-list', 'value'),
    State('scatter_chart', 'data'),
    State('error_chart', 'data'),
    State('line_chart', 'data'),
    allow_duplicate=True,
    prevent_initial_call= True
)
def get_selected_charts(n_clicks,chart_selection, scatter_chart, error_chart, line_chart):
    print(n_clicks)

    if n_clicks is None:
        raise PreventUpdate


    # order map
    order_map = {}

    # generate the right number of subplots based on user selection:
    rows = 0
    titles =[]
    row_heights =[]
    if 'cpa' in chart_selection:
        rows += 1
        titles.append("Combined Profile Area")
        row_heights.append(0.4)
        order_map.update({'cpa':[rows]})
    if 'line_plot' in chart_selection:
        rows += 1
        titles.append("Cross-Sectional Line Plot")
        row_heights.append(0.3)
        order_map.update({'line_plot': [rows]})
    if 'box_plot' in chart_selection:
        rows += 1
        titles.append("CPA Box Plot")
        row_heights.append(0.3)
        order_map.update({'error_plot': [rows]})


    subplot = make_subplots(rows=rows, cols=1, subplot_titles=titles,row_heights=row_heights, shared_xaxes=False)



    if n_clicks is None:
        return dash.no_update
    else:
        print(chart_selection)
        #print(charts)

        if 'cpa' in chart_selection:
            cpa_figure_data = scatter_chart.get("cpa")
            cpa_figure = go.Figure(json.loads(cpa_figure_data), layout=layout)
            # Update the x-axis formatting for the subplot to display dates

            row =order_map.get('cpa')

            for i in range(len(cpa_figure.data)):
                trace = cpa_figure.data[i]
                numeric_dates = trace.x
                # Convert numeric dates to datetime objects
                datetime_dates = [datetime.utcfromtimestamp(date * 24 * 60 * 60) for date in numeric_dates]
                # Format datetime dates as text using strftime (adjust the format as needed)
                formatted_dates = [date.strftime('%Y-%m-%d') for date in datetime_dates]
                trace.x  = formatted_dates



                subplot.add_trace(trace, row=row, col=1)


        if 'line_plot' in chart_selection:
            line_figure_data = line_chart.get("line_plot")
            line_figure = go.Figure(json.loads(line_figure_data))
            row = order_map.get('line_plot')

            for i in range(len(line_figure.data)):
                subplot.add_trace(line_figure.data[i], row=row, col=1)

        if 'box_plot' in chart_selection:
            error_figure_data = error_chart.get("error_plot")
            error_figure = go.Figure(json.loads(error_figure_data))
            row = order_map.get('error_plot')

            for i in range(len(error_figure.data)):
                subplot.add_trace(error_figure.data[i], row=row, col=1)

        # Save the subplot as an image
        img_bytes = subplot.to_image(format="png")
        # Create a BytesIO object
        img_io = io.BytesIO(img_bytes)
        # Encode the BytesIO object as base64
        encoding = base64.b64encode(img_io.read()).decode()

        #dcc.send_bytes(subplot.write_image, "figure.png")
    return subplot, dcc.send_bytes(img_bytes, filename='SWCM_Chart_Selection.png')
        # downloads as png



#@callback(Output('download', 'data'),
#          Input('download-charts-button', 'n_clicks'),
#          State("hidden-chart", "figure"),
#          prevent_initial_call=True,
#
#          )
#
#def download_figure(n_clicks, figure):
#    if n_clicks is None:
#        raise PreventUpdate
#
#    f = figure
#    # Create an in-memory buffer to save the PNG image
#    buffer = io.BytesIO()
#
#    pio.orca.config.format = 'png'
#
#    # Save the figure as a PNG image
#    pio.write_image(go.Figure(figure), buffer, format="png")
#
#    # Get the PNG image data from the buffer
#    png_data = buffer.getvalue()
#
#    # Encode the PNG data as a base64 string
#    encoded_png = base64.b64encode(png_data).decode('utf-8')
#
#    # Define the download filename and content
#    download_data = dict(content=encoded_png, filename="downloaded_figure.png")
#
#    return download_data
#














