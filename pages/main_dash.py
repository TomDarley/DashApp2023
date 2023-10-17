import dash
from dash import html, callback, Input, Output, State
from apps import scatter_plot
from apps import error_bar_plot
#from apps import mapbox
from apps import map_box_2
from apps import profile_line_plot
from apps import csa_table
import dash_bootstrap_components as dbc
from dash import dcc
from plotly.subplots import make_subplots
import json
import plotly.graph_objs as go
from datetime import datetime
from dash.exceptions import PreventUpdate


# register the page with dash giving url path
dash.register_page(__name__, path="/main_dash")

# define the layout of the main page
layout = html.Div(
    [
        dcc.Store(
            id="generated_charts",
            data={"cpa": None, "line_plot": None, "error_plot": None},
        ),
        dcc.Graph(id="hidden-chart", style={"display": "none"}),
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
                                            #html.H6(
                                            #    "Survey Unit Name:",
                                            #    className="card-title",
                                            #    style={
                                            #        "color": "blue",
                                            #        "margin-bottom": "5px",
                                            #    },
                                            #),

                                            html.Div("6aSU12", id="survey_unit_card"),


                                        ]
                                    )
                                ],
                                style={
                                    "margin": "10px",
                                    "border-radius": "10px",'box-shadow': '5px 5px 5px lightblue'
                                },

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
                                                },
                                            ),
                                            html.Div("----", id="trend_card"),
                                        ]
                                    )
                                ],
                                style={"margin": "10px", "border-radius": "10px",'box-shadow': '5px 5px 5px lightblue'}
,
                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Highest Recorded CPA:",
                                                className="card-title",
                                                style={
                                                    "color": "blue",
                                                    "margin-bottom": "5px",
                                                },
                                            ),
                                            html.Div("----", id="highest_card"),
                                        ]
                                    )
                                ],
                                style={"margin": "10px", "border-radius": "10px",'box-shadow': '5px 5px 5px lightblue'},
                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Lowest Recorded CPA:",
                                                className="card-title",
                                                style={
                                                    "color": "blue",
                                                    "margin-bottom": "5px",
                                                },
                                            ),
                                            html.Div("----", id="lowest_card"),
                                        ]
                                    )
                                ],
                                style={"margin": "10px", "border-radius": "10px",'box-shadow': '5px 5px 5px lightblue'},
                            ),
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            # html.H4("Download Charts:", className="card-title",
                                            #       style={'color': 'blue', 'margin-bottom': '10px', }),
                                            dcc.Checklist(
                                                id="download-check-list",
                                                options=[
                                                    {
                                                        "label": " CPA Plot ",
                                                        "value": "cpa",
                                                    },
                                                    {
                                                        "label": " Line Plot ",
                                                        "value": "line_plot",
                                                    },
                                                    {
                                                        "label": " Box Plot ",
                                                        "value": "box_plot",
                                                    },
                                                ],
                                                value=[],
                                            ),
                                            dbc.Button(
                                                "Download Charts",
                                                id="download-charts-button",
                                                n_clicks=0,
                                                size="sm",
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
                    ),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 2, "offset": 0},
                    xl={"size": 2, "offset": 0},
                    xxl={"size": 2, "offset": 0},
                    align="start",
                ),
                dbc.Col(
                    html.Div(
                        [
                            map_box_2.layout,
                        ],
                        style={"margin-top": "10px", "height": "60vh","border-radius": "10px", "overflow": "hidden"},
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
                    style={
                        "margin-top": "10px",
                        "height": "100%","border-radius": "10px", "overflow": "hidden"
                    },
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0},
                ),
            ],
            align="start",
            style={},
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
                    html.Div(profile_line_plot.layout),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 5, "offset": 0},
                    xl={"size": 5, "offset": 0},
                    xxl={"size": 5, "offset": 0},
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
                ),
                dbc.Col(
                    html.Div(csa_table.layout),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 10, "offset": 0},
                    xl={"size": 10, "offset": 0},
                    xxl={"size": 10, "offset": 0},
                ),
            ],
            align="start",
        ),
    ]
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

        label = label[0].split("-")[1].strip()
        return label  # Apply the className "fade-in-element" to initially hide the element


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
    Output("hidden-chart", "figure"),
    Output("download", "data"),
    Input("download-charts-button", "n_clicks"),
    State("download-check-list", "value"),
    State("scatter_chart", "data"),
    State("error_chart", "data"),
    State("line_chart", "data"),
    allow_duplicate=True,
    prevent_initial_call=True,
)
def get_selected_charts(
    n_clicks, chart_selection, scatter_chart, error_chart, line_chart
):
    """Function controls the logic behind which charts are to be downloaded using the download checklist"""

    if n_clicks is None:
        raise PreventUpdate

    # dict that stores the order of the selected maps to be downloaded
    order_map = {}

    # generate the right number of subplots based on user selection:
    rows = 0
    titles = []
    row_heights = []
    if "cpa" in chart_selection:
        rows += 1
        titles.append("Combined Profile Area")
        row_heights.append(0.4)
        order_map.update({"cpa": [rows]})
    if "line_plot" in chart_selection:
        rows += 1
        titles.append("Cross-Sectional Line Plot")
        row_heights.append(0.3)
        order_map.update({"line_plot": [rows]})
    if "box_plot" in chart_selection:
        rows += 1
        titles.append("CPA Box Plot")
        row_heights.append(0.3)
        order_map.update({"error_plot": [rows]})

    subplot = make_subplots(
        rows=rows,
        cols=1,
        subplot_titles=titles,
        row_heights=row_heights,
        shared_xaxes=False,
    )

    if rows == 1:
        subplot.update_layout(height=800, width=2000)
    elif rows == 2:
        subplot.update_layout(height=1500, width=2000)
    elif rows == 3:
        subplot.update_layout(height=2000, width=2000)

    if n_clicks is None:
        return dash.no_update
    else:
        if "cpa" in chart_selection:
            cpa_figure_data = scatter_chart.get("cpa")
            cpa_figure = go.Figure(json.loads(cpa_figure_data), layout=layout)

            # Update the x-axis formatting for the subplot to display dates
            row = order_map.get("cpa")

            for i in range(len(cpa_figure.data)):
                trace = cpa_figure.data[i]
                numeric_dates = trace.x

                # Convert numeric dates to datetime objects
                datetime_dates = [
                    datetime.utcfromtimestamp(date * 24 * 60 * 60)
                    for date in numeric_dates
                ]

                # Format datetime dates as text using strftime (adjust the format as needed)
                formatted_dates = [date.strftime("%Y-%m-%d") for date in datetime_dates]
                trace.x = formatted_dates
                subplot.add_trace(trace, row=row, col=1)

        if "line_plot" in chart_selection:
            line_figure_data = line_chart.get("line_plot")
            line_figure = go.Figure(json.loads(line_figure_data))
            row = order_map.get("line_plot")

            for i in range(len(line_figure.data)):
                subplot.add_trace(line_figure.data[i], row=row, col=1)

        if "box_plot" in chart_selection:
            error_figure_data = error_chart.get("error_plot")
            error_figure = go.Figure(json.loads(error_figure_data))
            row = order_map.get("error_plot")

            for i in range(len(error_figure.data)):
                subplot.add_trace(error_figure.data[i], row=row, col=1)

        # Save the subplot as an image
        img_bytes = subplot.to_image(format="png")

    return subplot, dcc.send_bytes(img_bytes, filename="SWCM_Chart_Selection.png")
